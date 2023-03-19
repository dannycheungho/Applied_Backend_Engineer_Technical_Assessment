from flask import Flask, jsonify, request
from src.models.models import Doctor, DoctorTranslation, District, DistrictTranslation, Category, CategoryTranslation, db
from sqlalchemy import exc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///doctors.db'
db.init_app(app)
default_language = 'en'

with app.app_context():
    #db.drop_all()  # debug mode only
    db.create_all()

@app.route('/doctor/<int:id>', methods=['GET'])
def get_doctor(id):
    doctor = Doctor.query.get(id)

    if doctor is None:
        return jsonify({'message': 'Doctor not found'}), 404

    result = handle_doctor_response(doctor, request.args)

    return jsonify(result)


@app.route('/doctor', methods=['POST'])
def create_doctor():
    data = request.json
    doctor = Doctor(name=data['name'], email=data['email'], phone=data['phone'])
    try:
        for district_data in data['districts']:
            district = District(district_name=district_data['district_name'],
                                address=district_data['address'],
                                clinic_phone=district_data['clinic_phone'],
                                price=district_data['price'],
                                price_remark=district_data['price_remark'] if district_data[
                                                                                'price_remark'] is not None else '',
                                working_time=district_data['working_time'])
            doctor.districts.append(district)

            for translation in district_data['district_translations']:
                district_translation = DistrictTranslation(language_id=translation['language_id'],
                                                        district_name=translation['district_name'],
                                                        address=translation['address'],
                                                        price_remark=translation['price_remark'])
                district_translation.district = district
                district.districtTranslation.append(district_translation)

        for category_data in data['categories']:
            category = Category(category_name=category_data["category_name"])
            doctor.categories.append(category)

        for category_translation_data in category_data["category_translations"]:
            category_translation = CategoryTranslation(language_id=category_translation_data["language_id"],
                                                    category_name=category_translation_data["category_name"])
            category.categoryTranslation.append(category_translation)

        for translation in data['doctor_translations']:
            doctor_translation = DoctorTranslation(language_id=translation['language_id'], name=translation['name'])
            doctor_translation.doctor = doctor
            doctor.doctorTranslation.append(doctor_translation)

        db.session.add(doctor)
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Doctor existed!'}) 

    return jsonify({'message': 'Doctor created successfully!'}), 201

@app.route('/doctor', methods=['GET'])
def get_all_doctors():
    doctors_query = Doctor.query
    
    doctors = doctors_query.all()
    result = []

    for doctor in doctors:
        if doctor is not None:
            if handle_doctor_response(doctor, request.args):
                result.append(handle_doctor_response(doctor, request.args))

    if not result:
        return jsonify({'message': 'Doctor record not found'}), 404

    return jsonify(result)

def handle_doctor_response(doctor, filter_condition):
    district_filter = filter_condition.get('district')
    category_filter = filter_condition.get('category')
    min_price_filter = filter_condition.get('min_price', type=int)
    max_price_filter = filter_condition.get('max_price', type=int)
    language_filter = filter_condition.get('language')
    
    if language_filter is None:
        language_filter = language_filter if language_filter is not None else default_language

    language_filter = language_country_code(language_filter)
    
    serialized_doctor = {
        'id': doctor.id,
        'name': doctor.name,
        'email': doctor.email,
        'phone': doctor.phone,
        'districts': []
    }

    for district in doctor.districts:
        if district_filter and district.district_name.name.upper() != district_filter.upper():
            continue
        if min_price_filter and district.price < min_price_filter:
            continue
        if max_price_filter and district.price > max_price_filter:
            continue
        
        serialized_district = {
            'id': district.id,
            'district_name': district.district_name.value[language_filter],
            'address': district.address,
            'clinic_phone': district.clinic_phone,
            'price': district.price,
            'price_remark': district.price_remark if district.price_remark is not None else '',
            'working_time': district.working_time
        }
        if language_filter is not None and language_filter != default_language:
            for translation in district.districtTranslation:
                if translation.language_id == language_filter:
                    serialized_district['address'] = translation.address
                    serialized_district['price_remark'] = translation.price_remark

            for translation in doctor.doctorTranslation:
                if translation.language_id == language_filter:
                    serialized_doctor['name'] = translation.name

        serialized_doctor['districts'].append(serialized_district)
    
    #serialized_doctor['categories'] = [category.category_name.value[language_filter] for category in doctor.categories]
    if category_filter is None:
        serialized_doctor['categories'] = [category.category_name.value[language_filter] for category in doctor.categories]
    else:
        serialized_doctor['categories'] = [category.category_name.value[language_filter] for category in doctor.categories if category.category_name.name == category_filter]

    if not serialized_doctor['districts'] or not serialized_doctor['categories']:
        return None 

    return serialized_doctor


def language_country_code(language_id):
    if language_id == 'en':
        return 0
    if language_id == 'cht':
        return 1
    return 0

if __name__ == "__main__":
    app.run(debug=True)
