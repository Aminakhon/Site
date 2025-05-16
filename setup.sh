cp sup_app.nginx.conf /etc/nginx/sites-available/sup_app.nginx.conf
cp template.db ./instance/site.db
certbot --nginx -d sup.silaeder.codingprojects.ru
