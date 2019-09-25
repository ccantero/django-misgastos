from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class UserCreateForm(UserCreationForm):

	class Meta:
		fields = ('username', 'email', 'password1', 'password2')
		model = get_user_model()

	def __init__(self,*args,**kwargs):
		super().__init__(*args, **kwargs)
		# Cristhian:
		# Label in the HTML
		# Optional
		#print(self.fields.keys())
		for key in self.fields.keys():
			self.fields[key].help_text = ""

		#print(self.fields['username'].help_text)
		self.fields['username'].label = 'Usuario'
		self.fields['email'].label = 'Correo Electronico'
		self.fields['password1'].label = 'Contraseña'
		self.fields['password2'].label = 'Confirmar contraseña'


