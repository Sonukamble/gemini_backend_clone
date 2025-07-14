from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from app.integrations.stripe import StripeClient
from app.db.session import SessionLocal
from app.models.subscription import Subscription, SubscriptionTierEnum
from app.core.logger import logger

class SubscriptionService:
    @staticmethod
    async def create_pro_subscription(user_id: int):
        """        
        Creates a Pro subscription for the user and returns the checkout URL.
        """
        try:
            checkout_url = await StripeClient.create_checkout_session(user_id)
            logger.info(f"Checkout session created for user {user_id}")
            return checkout_url
        except Exception as e:
            logger.error(f"Error creating Pro subscription for user {user_id}: {e}")
            raise Exception("Could not create Stripe checkout session")

    @staticmethod
    async def handle_webhook(payload, sig_header):
        """        Handles the Stripe webhook event.
        Verifies the signature and updates the subscription status in the database.
        """
        try:
            try:
                # Step 1: Verify the Stripe webhook signature
                event = StripeClient.verify_webhook(payload, sig_header)
            except ValueError as e:
                logger.error(f"Stripe webhook verification failed: {e}")
                return JSONResponse(status_code=400, content={"error": "Invalid signature"})
            
            # Step 2: Process the event
            if event["type"] == "checkout.session.completed":
                session = event["data"]["object"]
                user_id = session["metadata"].get("user_id")

                logger.info(f"Stripe checkout completed for user_id: {user_id}")

                try:
                    db: Session = SessionLocal()

                    # Step 3: Create or update subscription
                    subscription = db.query(Subscription).filter(Subscription.user_id == user_id).first()
                    if subscription:
                        subscription.tier = "Pro"
                        logger.info(f"Updated existing subscription to Pro for user {user_id}")
                    else:
                        new_subscription = subscription(user_id=user_id, tier="Pro")
                        db.add(new_subscription)
                        logger.info(f"Created new Pro subscription for user {user_id}")

                    db.commit()
                except Exception as db_error:
                    logger.error(f"Failed to update subscription in DB for user {user_id}: {db_error}")
                    return JSONResponse(status_code=500, content={"error": "Failed to update subscription"})
                finally:
                    db.close()

            return JSONResponse(status_code=200, content={"message": "Webhook processed successfully"})
        except Exception as e:
            logger.error(f"Error processing Stripe webhook: {e}")
            return JSONResponse(status_code=500, content={"error": "Failed to process webhook"})

    @staticmethod
    async def get_status(user_id: str):
        """        Retrieves the subscription status for a user.
        Returns the subscription tier (Basic or Pro).
        """
        db = SessionLocal()
        try:
            
            subscription = db.query(Subscription).filter(Subscription.user_id == user_id).first()
            tier=subscription.tier.value if subscription else SubscriptionTierEnum.basic.value

            logger.info(f"Fetched subscription tier '{tier}' for user {user_id}")

            if not subscription:
                return JSONResponse(content={"detail": "Not found"}, status_code=404)
            return subscription

        except Exception as e:
            logger.error(f"Error fetching subscription status for user {user_id}: {e}")
            return JSONResponse(
                status_code=500,
                content={"error": "Failed to retrieve subscription status"}
            )
        finally:
            db.close()
      