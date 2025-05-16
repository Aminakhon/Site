cp flask_app.nginx.conf /etc/nginx/sites-available/sup_app.nginx.conf
certbot --nginx -d silaeder.codingprojects.ru
