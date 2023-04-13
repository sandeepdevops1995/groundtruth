COMPOSE_IP_ADDRESS=${IP_ADDRESS}
COMPOSE_PORT=${PORT}
COMPOSE_SQL_USERNAME=${SQL_USERNAME}
COMPOSE_SQL_PASSOWRD=${SQL_PASSOWRD}
COMPOSE_SQL_IP=${SQL_IP}
COMPOSE_SQL_PORT=${SQL_PORT}
COMPOSE_SQL_DATABASE=${SQL_DATABASE}
COMPOSE_PSQL_USERNAME=${PSQL_USERNAME}
COMPOSE_PSQL_PASSOWRD=${PSQL_PASSOWRD}
COMPOSE_PSQL_IP=${PSQL_IP}
COMPOSE_PSQL_PORT=${PSQL_PORT}
COMPOSE_PSQL_DATABASE=${PSQL_DATABASE}
COMPOSE_WSDL_URL=${WSDL_URL}
COMPOSE_IAM_SERVICE_URL=${IAM_SERVICE_URL}
COMPOSE_LOGSTASH_IP=${LOGSTASH_IP}
COMPOSE_LOGSTASH_PORT=${LOGSTASH_PORT}
COMPOSE_DEBUG=${DEBUG}
COMPOSE_SQl_ECHO=${SQl_ECHO}
COMPOSE_PSQl_ECHO=${PSQl_ECHO}
COMPOSE_IS_MOCK_ENABLED=${IS_MOCK_ENABLED}
COMPOSE_IS_EVENT_BASED=${IS_EVENT_BASED}
COMPOSE_CCLS_GROUND_TRUTH=${CCLS_GROUND_TRUTH}

#remove .env file
rm -f ./.env

#read .env file in env folder
env_file_path="./env/.env"

_env_init(){

if ( [ $COMPOSE_IP_ADDRESS ] ) then 
    echo "ip address",${IP_ADDRESS}
else 
    env_compose_ip_address="$(sed -n -e 's/^.*IP_ADDRESS.*=//p' $env_file_path | tr -d \'\" | head -n 1 | tr -d ',' | xargs)"
    export IP_ADDRESS=$env_compose_ip_address
fi

if ( [ $COMPOSE_PORT ] ) then 
    echo "port",${PORT}
else 
    env_compose_port="$(sed -n -e 's/^.*PORT.*=//p' $env_file_path | tr -d \'\" | head -n 1 | tr -d ',' | xargs)"
    export PORT=$env_compose_port
fi

if ( [ $COMPOSE_SQL_USERNAME ] ) then 
    echo "sql username",${SQL_USERNAME}
else 
    env_compose_sql_username="$(sed -n -e 's/^.*SQL_USERNAME.*=//p' $env_file_path | tr -d \'\" | head -n 1 | tr -d ',' | xargs)"
    export SQL_USERNAME=$env_compose_sql_username
fi

if ( [ $COMPOSE_SQL_PASSOWRD ] ) then 
    echo "sql passowrd",${SQL_PASSOWRD}
else 
    env_compose_sql_password="$(sed -n -e 's/^.*SQL_PASSOWRD.*=//p' $env_file_path | tr -d \'\" | head -n 1 | tr -d ',' | xargs)"
    export SQL_PASSOWRD=$env_compose_sql_password
fi

if ( [ $COMPOSE_SQL_IP ] ) then 
    echo "sql ip",${SQL_IP}
else 
    env_compose_sql_ip="$(sed -n -e 's/^.*SQL_IP.*=//p' $env_file_path | tr -d \'\" | head -n 1 | tr -d ',' | xargs)"
    export SQL_IP=$env_compose_sql_ip
fi 

if ( [ $COMPOSE_SQL_PORT ] ) then 
    echo "sql port",${SQL_PORT}
else 
    env_compose_sql_port="$(sed -n -e 's/^.*SQL_PORT.*=//p' $env_file_path | tr -d \'\" | head -n 1 | tr -d ',' | xargs)"
    export SQL_PORT=$env_compose_sql_port
fi

if ( [ $COMPOSE_SQL_DATABASE ] ) then 
    echo "sql database",${SQL_DATABASE}
else 
    env_compose_sql_database="$(sed -n -e 's/^.*SQL_DATABASE.*=//p' $env_file_path | tr -d \'\" | head -n 1 | tr -d ',' | xargs)"
    export SQL_DATABASE=$env_compose_sql_database
fi

if ( [ $COMPOSE_PSQL_USERNAME ] ) then 
    echo "psql username",${PSQL_USERNAME}
else 
    env_compose_psql_username="$(sed -n -e 's/^.*PSQL_USERNAME.*=//p' $env_file_path | tr -d \'\" | head -n 1 | tr -d ',' | xargs)"
    export PSQL_USERNAME=$env_compose_psql_username
fi

if ( [ $COMPOSE_PSQL_PASSOWRD ] ) then 
    echo "psql password",${PSQL_PASSOWRD}
else 
    env_compose_psql_password="$(sed -n -e 's/^.*PSQL_PASSOWRD.*=//p' $env_file_path | tr -d \'\" | head -n 1 | tr -d ',' | xargs)"
    export PSQL_PASSOWRD=$env_compose_psql_password
fi

if ( [ $COMPOSE_PSQL_IP ] ) then 
    echo "psql ip",${PSQL_IP}
else 
    env_compose_psql_ip="$(sed -n -e 's/^.*PSQL_IP.*=//p' $env_file_path | tr -d \'\" | head -n 1 | tr -d ',' | xargs)"
    export PSQL_IP=$env_compose_psql_ip
fi 

if ( [ $COMPOSE_PSQL_PORT ] ) then 
    echo "psql port",${PSQL_PORT}
else 
    env_compose_psql_port="$(sed -n -e 's/^.*PSQL_PORT.*=//p' $env_file_path | tr -d \'\" | head -n 1 | tr -d ',' | xargs)"
    export PSQL_PORT=$env_compose_psql_port
fi

if ( [ $COMPOSE_PSQL_DATABASE ] ) then 
    echo "psql database",${PSQL_DATABASE}
else 
    env_compose_psql_database="$(sed -n -e 's/^.*PSQL_DATABASE.*=//p' $env_file_path | tr -d \'\" | head -n 1 | tr -d ',' | xargs)"
    export PSQL_DATABASE=$env_compose_psql_database
fi

if ( [ $COMPOSE_IAM_SERVICE_URL ] ) then 
    echo "iam service url",${IAM_SERVICE_URL}
else 
    env_iam_service_url="$(sed -n -e 's/^.*IAM_SERVICE_URL.*=//p' $env_file_path | tr -d \'\" | head -n 1 | tr -d ',' | xargs)"
    export IAM_SERVICE_URL=$env_iam_service_url
fi

if ( [ $COMPOSE_WSDL_URL ] ) then 
    echo "wsdl url",${WSDL_URL}
else 
    env_wsdl_url="$(sed -n -e 's/^.*WSDL_URL.*=//p' $env_file_path | tr -d \'\" | head -n 1 | tr -d ',' | xargs)"
    export WSDL_URL=$env_wsdl_url
fi

if ( [ $COMPOSE_LOGSTASH_IP ] ) then 
    echo "logstash ip",${LOGSTASH_IP}
else 
    env_logstash_ip="$(sed -n -e 's/^.*LOGSTASH_IP.*=//p' $env_file_path | tr -d \'\" | head -n 1 | tr -d ',' | xargs)"
    export LOGSTASH_IP=$env_logstash_ip
fi

if ( [ $COMPOSE_LOGSTASH_PORT ] ) then 
    echo "logstash port",${LOGSTASH_PORT}
else 
    env_logstash_port="$(sed -n -e 's/^.*LOGSTASH_PORT.*=//p' $env_file_path | tr -d \'\" | head -n 1 | tr -d ',' | xargs)"
    export LOGSTASH_PORT=$env_logstash_port
fi

if ( [ $COMPOSE_DEBUG ] ) then 
    echo "debug",${DEBUG}
else 
    env_debug="$(sed -n -e 's/^.*DEBUG.*=//p' $env_file_path | tr -d \'\" | head -n 1 | tr -d ',' | xargs)"
    export DEBUG=$env_debug
fi

if ( [ $COMPOSE_SQl_ECHO ] ) then 
    echo "sql echo",${SQl_ECHO}
else 
    env_sql_echo="$(sed -n -e 's/^.*SQl_ECHO.*=//p' $env_file_path | tr -d \'\" | head -n 1 | tr -d ',' | xargs)"
    export SQl_ECHO=$env_sql_echo
fi

if ( [ $COMPOSE_PSQl_ECHO ] ) then 
    echo "psql echo",${PSQl_ECHO}
else 
    env_psql_echo="$(sed -n -e 's/^.*PSQl_ECHO.*=//p' $env_file_path | tr -d \'\" | head -n 1 | tr -d ',' | xargs)"
    export PSQl_ECHO=$env_psql_echo
fi

if ( [ $COMPOSE_IS_MOCK_ENABLED ] ) then 
    echo "is mock enabled",${IS_MOCK_ENABLED}
else 
    env_is_mock_enabled="$(sed -n -e 's/^.*IS_MOCK_ENABLED.*=//p' $env_file_path | tr -d \'\" | head -n 1 | tr -d ',' | xargs)"
    export IS_MOCK_ENABLED=$env_is_mock_enabled
fi

if ( [ $COMPOSE_IS_EVENT_BASED ] ) then 
    echo "is event based",${IS_EVENT_BASED}
else 
    env_is_event_based="$(sed -n -e 's/^.*IS_EVENT_BASED.*=//p' $env_file_path | tr -d \'\" | head -n 1 | tr -d ',' | xargs)"
    export IS_EVENT_BASED=$env_is_event_based
fi

if ( [ $COMPOSE_CCLS_GROUND_TRUTH ] ) then 
    echo "ccls ground truth",${CCLS_GROUND_TRUTH}
else 
    env_ccls_ground_truth="$(sed -n -e 's/^.*CCLS_GROUND_TRUTH.*=//p' $env_file_path | tr -d \'\" | head -n 1 | tr -d ',' | xargs)"
    export CCLS_GROUND_TRUTH=$env_ccls_ground_truth
fi

}
_env_init