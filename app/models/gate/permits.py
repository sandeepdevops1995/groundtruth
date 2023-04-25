from app import postgres_db as db

class Permit(db.Model):
    # currently using fields
    permit_no = db.Column(db.String(50),primary_key=True)
    permit_date = db.Column(db.DateTime())
    permit_expiry_date = db.Column(db.DateTime())
    container_no = db.Column(db.String(50))
    container_size = db.Column(db.String(50)) 
    container_type = db.Column(db.String(50))
    container_status = db.Column(db.String(50))         #permit_details
    container_life_no = db.Column(db.DateTime())        #permit details
    hazard_status = db.Column(db.Boolean())
    damage_status = db.Column(db.Boolean())
    sline_code = db.Column(db.String(50))               #permit_details
    sline_no = db.Column(db.String(50))
    crn_no = db.Column(db.String(50))
    seal_count = db.Column(db.Integer())
    seal_no = db.Column(db.String(50))
    seal_type = db.Column(db.String(50))
    vehicle_no =  db.Column(db.String(50))
    gate_in_time = db.Column(db.DateTime())
    gate_out_time = db.Column(db.DateTime())
    user_id = db.Column(db.String(50))
    gate_no = db.Column(db.String(3))
    stk_loc = db.Column(db.String(20))
    damage_code = db.Column(db.String(20))
    dt_seal = db.Column(db.DateTime())
    
    #Fields may require in future
    permit_type = db.Column(db.String(50))
    container_type = db.Column(db.String(50))
    iso_code = db.Column(db.String(50))
    liner_seal = db.Column(db.String(50))
    custom_seal = db.Column(db.String(50), nullable=True)
    reefer = db.Column(db.String(50), nullable=True)
    is_empty_or_laden = db.Column(db.String(10))
    cargo_type = db.Column(db.String(50))
    POD = db.Column(db.String(50))
    permit_details = db.Column(db.Text)
    bill_info = db.Column(db.Text)
    truck = db.Column(db.Text)
    hazard = db.Column(db.Text)
    un_number = db.Column(db.Text)