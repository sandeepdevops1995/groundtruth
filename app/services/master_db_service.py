from app import postgres_db as db
from app.models import *
from app.services.decorator_service import query_debugger
import app.constants as Constants
from app.logger import logger
import config
from app.constants import GroundTruthType
from app.services.rake.gt_upload_service import commit
import time
from app.models.utils import db_format,db_functions


class MasterData():
    @query_debugger()
    def create_iso_code(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =ISOcode(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_iso_code(count,isRetry)
                
                
    @query_debugger()
    def get_iso_code(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = ISOcode.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_iso_code(count,isRetry)
                
    @query_debugger()
    def create_ctr_size(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =CtrSize(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_ctr_size(count,isRetry)
                
    @query_debugger()
    def get_ctr_size(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = CtrSize.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_ctr_size(count,isRetry)
    
    @query_debugger()
    def create_country(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =Ctry(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_country(count,isRetry)           
                
    @query_debugger()
    def get_country(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = Ctry.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_country(count,isRetry)
                
    @query_debugger()
    def create_country_custom(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =CtryCustom(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_country_custom(count,isRetry)
                
    @query_debugger()
    def get_country_custom(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = CtryCustom.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_country_custom(count,isRetry)
                
                
    @query_debugger()
    def create_cha_custom(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =ChaCustom(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_cha_custom(count,isRetry)
                
    @query_debugger()
    def get_cha_custom(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = ChaCustom.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_cha_custom(count,isRetry)
                
    @query_debugger()
    def create_cha(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =Cha(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_cha(count,isRetry)
                
    @query_debugger()
    def get_cha(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = Cha.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_cha(count,isRetry)
                
    @query_debugger()
    def create_cha_directory(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =ChaDirectory(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_cha_directory(count,isRetry)
                           
    @query_debugger()
    def get_cha_directory(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = ChaDirectory.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_cha_directory(count,isRetry)
                   
    @query_debugger()
    def create_impr_expr_custom(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =ImprExprCustom(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_impr_expr_custom(count,isRetry)
    
    @query_debugger()
    def get_impr_expr_custom(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = ImprExprCustom.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_impr_expr_custom(count,isRetry)
                   
    @query_debugger()
    def create_port_custom(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =PortCustom(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_port_custom(count,isRetry)
    
    @query_debugger()
    def get_port_custom(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = PortCustom.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_port_custom(count,isRetry)
                   
    
    @query_debugger()
    def create_cust_email(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =CustEmail(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_cust_email(count,isRetry)
    
    @query_debugger()
    def get_cust_email(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = CustEmail.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_cust_email(count,isRetry)
                   
    @query_debugger()
    def create_cust_dtls(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =CustDtls(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_cust_dtls(count,isRetry)
    
    @query_debugger()
    def get_cust_dtls(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = CustDtls.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_cust_dtls(count,isRetry)
                   
    @query_debugger()
    def create_agency(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =Agency(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_agency(count,isRetry)
    
    @query_debugger()
    def get_agency(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = Agency.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_agency(count,isRetry)
                   
    @query_debugger()
    def create_bl_whrf(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =BlWhrf(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_bl_whrf(count,isRetry)
    
    @query_debugger()
    def get_bl_whrf(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = BlWhrf.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_bl_whrf(count,isRetry)
    
    @query_debugger()
    def create_cfs(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =Cfs(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_cfs(count,isRetry)
                   
    @query_debugger()
    def get_cfs(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = Cfs.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_cfs(count,isRetry)
    
    @query_debugger()
    def create_concor_wagon_details(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =CncrWgnDtls(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_concor_wagon_details(count,isRetry)
                   
    @query_debugger()
    def get_concor_wagon_details(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = CncrWgnDtls.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_concor_wagon_details(count,isRetry)
                   
    @query_debugger()
    def create_consolidator(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =Cnsldtor(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_consolidator(count,isRetry)
    
    @query_debugger()
    def get_consolidator(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = Cnsldtor.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_consolidator(count,isRetry)
                   
    @query_debugger()
    def create_container_tare_weight(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =CtrTarewt(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_container_tare_weight(count,isRetry)
    
    @query_debugger()
    def get_container_tare_weight(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = CtrTarewt.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_container_tare_weight(count,isRetry)
    
    @query_debugger()
    def create_container_details(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =CtrDtls(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_container_details(count,isRetry)
                   
    @query_debugger()
    def get_container_details(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = CtrDtls.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_container_details(count,isRetry)
                   
    @query_debugger()
    def create_equipment_details(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =EqptDtls(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_equipment_details(count,isRetry)
    
    @query_debugger()
    def get_equipment_details(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = EqptDtls.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_equipment_details(count,isRetry)
                   
    @query_debugger()
    def create_equipment_master(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =EqptMst(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_equipment_master(count,isRetry)
    
    @query_debugger()
    def get_equipment_master(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = EqptMst.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_equipment_master(count,isRetry)
                   
    @query_debugger()
    def create_error_messages(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =ErrorMessages(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_error_messages(count,isRetry)
                
    @query_debugger()
    def get_error_messages(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = ErrorMessages.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_error_messages(count,isRetry)
    
    @query_debugger()
    def create_gateway_port(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =Gwport(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_gateway_port(count,isRetry)
                   
    @query_debugger()
    def get_gateway_port(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = Gwport.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_gateway_port(count,isRetry)
                   
    @query_debugger()
    def create_gateway_port_state(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =GwportState(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_gateway_port_state(count,isRetry)
    
    @query_debugger()
    def get_gateway_port_state(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = GwportState.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_gateway_port_state(count,isRetry)
                   
    @query_debugger()
    def create_cha_email(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =ChaEmail(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_cha_email(count,isRetry)
    
    @query_debugger()
    def get_cha_email(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = ChaEmail.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_cha_email(count,isRetry)
                   
    @query_debugger()
    def create_hld_track(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =HldTrack(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_hld_track(count,isRetry)
    
    @query_debugger()
    def get_hld_track(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = HldTrack.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_hld_track(count,isRetry)
                   
    @query_debugger()
    def create_handling(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =Hndg(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_handling(count,isRetry)
    
    @query_debugger()
    def get_handling(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = Hndg.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_handling(count,isRetry)
                   
    @query_debugger()
    def create_handling_activity(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =HndgActy(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_handling_activity(count,isRetry)
    
    @query_debugger()
    def get_handling_activity(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = HndgActy.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_handling_activity(count,isRetry)
                   
    @query_debugger()
    def create_package(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =Pkg(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_package(count,isRetry)
    
    @query_debugger()
    def get_package(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = Pkg.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_package(count,isRetry)
                   
    @query_debugger()
    def create_user_filing(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =UsrFiling(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_user_filing(count,isRetry)
    
    @query_debugger()
    def get_user_filing(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = UsrFiling.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_user_filing(count,isRetry)
                   
    @query_debugger()
    def create_wagon_master(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =WgnMst(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_wagon_master(count,isRetry)
    
    @query_debugger()
    def get_wagon_master(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = WgnMst.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_wagon_master(count,isRetry)
                   
    @query_debugger()
    def create_wagon_master_etms(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =WgnMstEtms(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_wagon_master_etms(count,isRetry)
    
    @query_debugger()
    def get_wagon_master_etms(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = WgnMstEtms.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_wagon_master_etms(count,isRetry)
                
    @query_debugger()
    def create_bl_acty(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =BlActy(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_bl_acty(count,isRetry)
                   
    @query_debugger()
    def get_bl_acty(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = BlActy.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_bl_acty(count,isRetry)
                
    @query_debugger()
    def create_port_conv(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =PortConv(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_port_conv(count,isRetry)
                
                
    @query_debugger()
    def get_port_conv(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = PortConv.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_port_conv(count,isRetry)
                   
    @query_debugger()
    def create_station(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =Station(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_station(count,isRetry)
    
    @query_debugger()
    def get_station(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = Station.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_station(count,isRetry)
                   
    @query_debugger()
    def create_module_cd(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =ModuleCd(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_module_cd(count,isRetry)
    
    @query_debugger()
    def get_module_cd(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = ModuleCd.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_module_cd(count,isRetry)
                   
    @query_debugger()
    def create_gateway_port_conv(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =GwPortConv(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_gateway_port_conv(count,isRetry)
    
    @query_debugger()
    def get_gateway_port_conv(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = GwPortConv.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_gateway_port_conv(count,isRetry)
                   
    @query_debugger()
    def create_cfs_conv(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =CfsConv(**data)
            db.session.add(record)
            commit()
            return True
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_cfs_conv(count,isRetry)
    
    @query_debugger()
    def get_cfs_conv(count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            data = CfsConv.query.all()
            return db_functions(data).as_json()
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_cfs_conv(count,isRetry)
                
    @query_debugger()
    def create_track_master_details(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            record =TrackDetails(**data)
            db.session.add(record)
            return commit()
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_track_master_details(count,isRetry)

    
    @query_debugger()
    def get_track_master_details(filter_data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            if filter_data:
                track_data = TrackDetails.query.filter_by(**filter_data).all()
                return track_data
            data = TrackDetails.query.all()
            return data
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_track_master_details(count,isRetry)

    @query_debugger()
    def create_container_stat_details(data,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            for each in data:
                record = CtrStat(**each)
                db.session.add(record)
            return commit()
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.create_container_stat_details(count,isRetry)

    
    @query_debugger()
    def get_container_stat_details(filter_data=None,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                pass
            if filter_data:
                data = CtrStat.query.filter_by(**filter_data).all()
                return data
            data = CtrStat.query.all()
            return data
            
        except Exception as e:
            logger.error('Error while querying database\n : {}'.format(str(e)))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                MasterData.get_container_stat_details(count,isRetry)
