from otp.models import OTP


def check_otp_request(user, data, check_for_is_active=False):
    otp_for: str = data["otp_for"]
    if check_for_is_active:
        check = {
            OTP.EMAIL: "is_email_activated",
            OTP.PHONE: "is_phone_activated"
        }[otp_for]
        return getattr(user, check)

    check = {
        OTP.EMAIL: "email",
        OTP.PHONE: "phone"
    }[otp_for]
    return getattr(user, check), otp_for.lower()

