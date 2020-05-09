# Sposób Mateusza na walidacje formularza Donation


# from donation.models import Donation
#
#
# class DonationFormValidator:
#     @staticmethod
#     def validate_data(**kwargs):
#         # jak nie idzie okej albo cos zle
#         # return False, msg
#
#         return True, None
#
#
# class DonationFormCreator:
#     @staticmethod
#     def create(user_id, **kwargs):
#         donation = Donation.objects.create(quantity=bags_quantity,
#                                            institution_id=institution_id,
#                                            address=address,
#                                            city=city,
#                                            zip_code=postcode,
#                                            phone_number=phone,
#                                            pick_up_date=date,
#                                            pick_up_time=time,
#                                            pick_up_comment=more_info,
#                                            user_id=user_id)
#         donation.categories.add(*category_id_list)
#         donation.save()
#         return donation
