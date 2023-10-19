from rest_framework import serializers
from .models import user_data

class userSeralizer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    Email = serializers.EmailField()
    Password = serializers.CharField()

    def create(self, data):
        # required, password should have atleast 1 special character, 1 uppercase, 1 number, minlength 8
        # isUpperCase = False
        # isNumber = False
        # for i in str(data.password):
        specialCharectors = ['!','@','#','$','%','^','&','*']
        special_bool = False
        number_bool = False
        isupper_bool = False
        for i in data['Password']:
            if i in specialCharectors:
                special_bool = True
            if str(i).isupper():
                isupper_bool = True
            if str(i).isdigit():
                number_bool = True
        if len(data['Password']) > 8 and special_bool and isupper_bool and number_bool:
            pass
        else:
            return 'Invalid Password'
        
        if len(data['Email'].split('@')) > 1 and len(data['Email'].split('@')[1].split('.')) > 1:
            pass
        else:
            return 'Invalid Email'
        user_data.objects.create(**data)
        return 'Success'

    def update(self, instance, data):
        specialCharectors = ['!','@','#','$','%','^','&','*']
        special_bool = False
        number_bool = False
        isupper_bool = False
        for i in data['Password'].value:
            if i in specialCharectors:
                special_bool = True
            if str(i).isupper():
                isupper_bool = True
            if str(i).isdigit():
                number_bool = True
        if len(data['Password'].value) > 7 and special_bool and isupper_bool and number_bool:
            pass
        else:
            return 'Invalid Password'
        instance.first_name = data['first_name'].value
        if data['last_name'].value:
            instance.last_name = data['last_name'].value
        if len(data['Email'].value.split('@')) > 1 and len(data['Email'].value.split('@')[1].split('.')) > 1:
            instance.Email = data['Email'].value
        else:
            return 'Invalid Email'
        instance.Password = data['Password'].value
        instance.save()
        return 'Success'
    
    class Meta:
        model = user_data
        fields = [ 'first_name', 'last_name', 'Email', 'Password']