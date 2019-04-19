docker run -p 80:80 \
            -e "PGADMIN_DEFAULT_EMAIL=user@domain.com" \
            -e "PGADMIN_DEFAULT_PASSWORD=SuperSecret" \
            --network=flask_network \
            -d dpage/pgadmin4 \
            --name pgadmin4
