class Uploader:
    @staticmethod
    def upload_photo_for_product(instance, filename):
        return f"product/{filename}"

    @staticmethod
    def upload_photo_for_business_profile(instance, filename):
        return f"business-profile/{filename}"

    @staticmethod
    def upload_photo_for_notification(instance, filename):
        return f"notification/{filename}"