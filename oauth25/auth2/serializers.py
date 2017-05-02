#from rest_framework import serializers


from auth2.models import BPInformation, BPDataList, UserInformation, HRDataInformation, CurrentHRInformation

# class BPInformationSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = BPInformation
# 		fields = ('NextPageUrl', 'CurrentRecordCount', 'RecordCount', 'BPUnit', 'PageLength', 'PrevPageUrl', 'PageNumber', 'user')