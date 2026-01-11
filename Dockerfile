FROM jekyll/jekyll AS build

RUN mkdir /nonnowebsite
COPY . /nonnowebsite
WORKDIR /nonnowebsite

RUN chmod 644 /nonnowebsite/assets/images/*
RUN chown -R jekyll /nonnowebsite

RUN bundle install && bundle exec jekyll build -d public


FROM nginx

COPY --from=build /nonnowebsite/public/ /usr/share/nginx/html/
