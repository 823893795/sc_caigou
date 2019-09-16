from flask import Blueprint, render_template

bp = Blueprint('bp', __name__)


@bp.route('/index', methods=['GET'])
def index():
    from app.models import ProvinceInfo, CityInfo
    pro_list = ProvinceInfo.query.order_by(ProvinceInfo.purchase_time.desc(), ProvinceInfo.create_time.desc()).all()
    city_list = CityInfo.query.order_by(CityInfo.purchase_time.desc(), CityInfo.create_time.desc()).all()
    return render_template('index.html', pro_list=pro_list, city_list=city_list)