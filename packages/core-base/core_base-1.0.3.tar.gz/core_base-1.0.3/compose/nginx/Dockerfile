 # nginx镜像compose/nginx/Dockerfile

FROM nginx:latest

 # 删除原有配置文件，创建静态资源文件夹和ssl证书保存文件夹
RUN rm /etc/nginx/conf.d/default.conf \
 && mkdir -p /home/nginx/data \
 && mkdir -p /home/nginx/run \
 && mkdir -p /home/nginx/log \
 && mkdir -p /usr/share/nginx/html/media \
 && mkdir -p /usr/share/nginx/html/static \
 && mkdir -p /usr/share/nginx/html/media \
 && mkdir -p /usr/share/nginx/ssl \
 && groupadd  module \
 && usermod nginx -g  module \
 && chmod -R 777 /etc/ /var/ /usr/ /home/nginx/ \
 && chown nginx:module -R /etc/ /var /usr/ /home/nginx/

# 设置Media文件夹用户和用户组为Linux默认www-data, 并给予可读和可执行权限,
# 否则用户上传的图片无法正确显示。
RUN chown -R www-data:www-data /usr/share/nginx/html \
 && chmod -R 775 /usr/sbin/ /usr/share/nginx/html/
USER nginx
# 添加配置文件
ADD ./nginx.conf /etc/nginx/
ADD ./default.conf /etc/nginx/conf.d/
COPY ./html /usr/share/nginx/html
COPY ./static /usr/share/nginx/html/teamwork/static/
COPY ./ssl /usr/share/nginx/ssl/
WORKDIR /usr/share/nginx/html/
# 关闭守护模式
CMD ["nginx", "-g", "daemon off;"]