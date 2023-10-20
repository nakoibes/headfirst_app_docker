init-run:
	docker compose up -d
	sleep 10
	docker compose exec -T mysql-headfirst sh -c "mysql -u root -p$(MYSQL_ROOT_PASSWORD) $(MYSQL_DATABASE) < /sql_scripts/create_table_log.sql"
run:
	docker compose up -d
dump-db:
	docker compose exec -T mysql-headfirst sh -c "mysql -u root -p$(MYSQL_ROOT_PASSWORD) $(MYSQL_DATABASE) < /sql_scripts/dump.sql"
remove:
	docker stop app_headfirst mysql_headfirst
	docker rm app_headfirst mysql_headfirst
	#docker rmi hearfirst_app_docker-app-headfirst hearfirst_app_docker-mysql-headfirst
start-db:
	docker run --name mysql --env-file .env -d -p 6000:3306  -v /home/nakoibes/hearfirst_app_docker/db_data:/var/lib/mysql mysql
stop-db:
	docker stop mysql
remove-db:
	docker stop mysql
	docker rm mysql
run-dev:
	docker build -t headapp .
	docker run -d -p 5000:5000 --name headapp --env-file .env -v /home/nakoibes/hearfirst_app_docker:/app  headapp
stop-dev:
	docker stop headapp
	docker rm headapp
