import stripe
from config import Config
from core.logger import logger

stripe.api_key = Config.STRIPE_SECRET_KEY
endpoint_secret = Config.STRIPE_WEBHOOK_SECRET

class StripeClient:

    @staticmethod
    def create_checkout_session(user_id: int):
        """        
        Creates a Stripe checkout session for a Pro subscription.
        Returns the checkout URL.
        """
        try:

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': Config.STRIPE_PRO_PRICE_ID,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=f"{Config.FRONTEND_URL}/success",  
                cancel_url=f"{Config.FRONTEND_URL}/cancel",  
                metadata={"user_id": str(user_id)}
            )
            logger.info(f"Stripe checkout session created for user {user_id}")
            return session.url
        except Exception as e:
            logger.error(f"Stripe session creation failed for user {user_id}: {e}")
            raise Exception(f"Stripe checkout session creation failed: {e}")

    @staticmethod
    def verify_webhook(payload, sig_header):
        """        Verifies the Stripe webhook signature.
        Returns the event object if verification is successful.
        """
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
            return event
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Webhook signature verification failed: {e}")
            raise ValueError("Invalid signature")
        
