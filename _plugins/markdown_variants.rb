require "fileutils"

def write_markdown(site, url, content)
  relative = url.sub(%r{\A/}, "")
  path = if relative.empty?
           File.join(site.dest, "index.md")
         elsif relative.end_with?("/")
           File.join(site.dest, relative, "index.md")
         else
           File.join(site.dest, relative.sub(/\.[^.]+\z/, ".md"))
         end

  FileUtils.mkdir_p(File.dirname(path))
  File.write(path, content.strip + "\n")
end

Jekyll::Hooks.register :site, :post_write do |site|
  posts = site.posts.docs
  links = posts.map { |post| "- [#{post.data["title"]}](#{post.url}) — #{post.date.strftime("%Y-%m-%d")}" }.join("\n")

  write_markdown(site, "/", <<~MARKDOWN)
    # NonnoAlex — Alessandro Lo Manto
    > Head of DevOps & Infrastructure working on production systems, distributed infrastructure, and secure environments for AI agents.

    Alessandro runs production for [Osmosis](https://osmosis.zone) and writes about keeping distributed systems available, observable, and recoverable.

    ## Writing
    #{links}

    ## Start here
    - [About](/about/)
    - [Contact](/contact/)
    - [Privacy](/privacy/)
    - [Agent instructions](/llms.txt)
  MARKDOWN

  write_markdown(site, "/blog/", "# Blog\n\n> Notes on running things in production.\n\n#{links}")
  write_markdown(site, "/blog/archive/", "# Blog archive\n\n#{links}")

  posts.each do |post|
    write_markdown(site, post.url, "# #{post.data["title"]}\n\nPublished #{post.date.strftime("%Y-%m-%d")}\n\n#{post.content}")
  end

  site.pages.select { |page| page.data["markdown_variant"] }.each do |page|
    write_markdown(site, page.url, "# #{page.data["title"]}\n\n#{page.content}")
  end
end
