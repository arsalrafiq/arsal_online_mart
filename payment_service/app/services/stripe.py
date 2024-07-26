# app/services/stripe.py
import stripe
from app.core.config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

async def create_payment_intent(amount: int, currency: str = "USD"):
    try:
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
        )
        return intent
    except stripe.error.StripeError as e:
        # Handle Stripe errors
        raise ValueError(f"Stripe error: {str(e)}")