# En serializers.py
from rest_framework import serializers
from .models import RegistrationForm

class RegistrationFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationForm
        fields = '__all__'
        # Deja read_only como estaba, está bien
        extra_kwargs = {
            'user': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            # Puedes añadir required=False a campos que NO son obligatorios siempre
            # 'campo_opcional': {'required': False},
        }

    def validate(self, data):
        # --- Ejecuta la validación compleja SOLO si NO es una solicitud PATCH ---
        if not self.partial:
            # Obtener el valor de is_regulated_subject (puede no estar si es PUT y no se envía)
            # Si es PUT, necesitamos el valor existente de la instancia.
            # Si es POST, debe estar en data.
            instance = getattr(self, 'instance', None)
            is_regulated_subject = data.get('is_regulated_subject', getattr(instance, 'is_regulated_subject', None))

            # Validar que is_regulated_subject tenga un valor ('si' o 'no') para POST/PUT
            if is_regulated_subject not in ['si', 'no']:
                 # Si es POST (no hay instancia), es requerido
                 if not instance:
                     raise serializers.ValidationError({'is_regulated_subject': "This field is required."})
                 # Si es PUT pero no se proporcionó, está bien (se usa el de la instancia)
                 # Pero si se proporcionó y es inválido, lanzar error.
                 elif 'is_regulated_subject' in data:
                      raise serializers.ValidationError({'is_regulated_subject': "Must specify 'si' or 'no'"})
                 # Si es PUT y no se proporcionó, usa el valor de la instancia para la lógica siguiente

            # --- INICIO DE LA LÓGICA ORIGINAL (dentro del if not self.partial) ---
            if is_regulated_subject == 'si':
                required_fields = {
                    'regulated_subject_type': "Regulated subject type is required",
                    'registration_code': "Registration code is required for regulated subjects"
                }

                for field, message in required_fields.items():
                    # Para POST/PUT, el campo debe existir y tener valor
                    if not data.get(field): # .get maneja si la clave no está en data
                        raise serializers.ValidationError({field: message})

                # Clear inapplicable field - Esto está bien, si se envía en PUT se limpia
                if 'employment_condition' in data:
                    data['employment_condition'] = None # O elimínalo: data.pop('employment_condition', None)

                # Specific validation by subject type
                subject_type = data.get('regulated_subject_type')
                if subject_type == 'Intermediary' and not data.get('intermediary_type'):
                    raise serializers.ValidationError({'intermediary_type': "Must specify the intermediary type"})
                elif subject_type == 'Auxiliary' and not data.get('auxiliary_type'):
                    raise serializers.ValidationError({'auxiliary_type': "Must specify the auxiliary type"})
                elif subject_type == 'Auditor Externo' and not data.get('auditor_type'):
                     raise serializers.ValidationError({'auditor_type': "Must specify the auditor type"})

            elif is_regulated_subject == 'no':
                # Validation for non-regulated subjects
                if not data.get('employment_condition'): # Requerido para no regulados en POST/PUT
                    raise serializers.ValidationError({'employment_condition': "Must specify your employment condition"})

                # Clear inapplicable fields - Esto está bien
                clearable_fields = [
                    'regulated_subject_type', 'intermediary_type', 'auxiliary_type',
                    'auditor_type', 'registration_code'
                ]
                for field in clearable_fields:
                    if field in data: # Solo limpiar si se envió explícitamente en PUT
                         data[field] = None # O usa pop: data.pop(field, None)

            # --- FIN DE LA LÓGICA ORIGINAL ---

        # Puedes añadir validaciones que apliquen SIEMPRE (POST, PUT, PATCH) aquí fuera del if
        # Por ejemplo, si el estado 'aceptado' requiere alguna otra condición simple:
        # if data.get('state') == 'aceptado' and not self.instance.some_other_field:
        #    raise serializers.ValidationError({'state': 'Cannot accept without condition X.'})

        return data # Siempre retorna los datos validados