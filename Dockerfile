FROM jekyll/jekyll AS build

WORKDIR /nonnowebsite
COPY Gemfile Gemfile.lock ./
RUN bundle install
COPY . .
RUN bundle exec jekyll build -d public


FROM nginx

COPY --from=build /nonnowebsite/public/ /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf
