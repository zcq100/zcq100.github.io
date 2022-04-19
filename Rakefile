# adapted from https://github.com/imathis/octopress/blob/master/Rakefile
# usage rake new_post['My New Post'] or rake new_post (defaults to "My New Post")
desc 'Start a new post'
task :new, :title do |_t, args|
  args.with_defaults(title: 'My New Post')
  title = args.title
  filename = "_posts/#{Time.now.strftime('%Y-%m-%d')}-#{title.downcase.gsub(/&/, 'and').gsub(/[,'":?!()\[\]]/, '').gsub(/[\W.]/, '-').gsub(
    /-+$/, ''
  )}.md"
  puts "Creating new post: #{filename}"
  open(filename, 'w') do |post|
    post.puts '---'
    post.puts 'layout: posts'
    post.puts "title: \"#{title.gsub(/&/, '&amp;')}\""
    post.puts 'description: '
    post.puts 'headline: '
    post.puts "modified: #{Time.now}"
    post.puts 'category: personal'
    post.puts 'tags: []'
    post.puts 'image: '
    post.puts '  feature: '
    post.puts 'comments: true'
    post.puts 'mathjax: '
    post.puts '---'
  end
end

desc 'Start a new quote'
task :newquote, :title do |_t, args|
  args.with_defaults(title: 'My New quote')
  title = args.title
  filename = "_posts/#{Time.now.strftime('%Y-%m-%d')}-#{title.downcase.gsub(/&/, 'and').gsub(/[,'":?!()\[\]]/, '').gsub(/[\W.]/, '-').gsub(
    /-+$/, ''
  )}.md"
  puts "Creating new post: #{filename}"
  open(filename, 'w') do |post|
    post.puts '---'
    post.puts 'layout: post'
    post.puts 'type: quote'
    post.puts "title: \"#{title.gsub(/&/, '&amp;')}\""
    post.puts 'description: '
    post.puts 'headline: '
    post.puts "modified: #{Time.now}"
    post.puts 'category: quotes'
    post.puts 'tags: []'
    post.puts 'image: '
    post.puts '  feature: '
    post.puts 'comments: false'
    post.puts 'mathjax: '
    post.puts '---'
  end
end

desc 'Start a new status'
task :newstatus, :title do |_t, args|
  args.with_defaults(title: 'My New Post')
  title = args.title
  filename = "_posts/#{Time.now.strftime('%Y-%m-%d')}-#{title.downcase.gsub(/&/, 'and').gsub(/[,'":?!()\[\]]/, '').gsub(/[\W.]/, '-').gsub(
    /-+$/, ''
  )}.md"
  puts "Creating new post: #{filename}"
  open(filename, 'w') do |post|
    post.puts '---'
    post.puts 'layout: posts'
    post.puts 'type: status'
    post.puts "title: \"#{title.gsub(/&/, '&amp;')}\""
    post.puts 'description: '
    post.puts 'headline: '
    post.puts "modified: #{Time.now}"
    post.puts 'category: status'
    post.puts 'tags: []'
    post.puts 'image: '
    post.puts '  feature: '
    post.puts 'comments: false'
    post.puts 'mathjax: '
    post.puts '---'
  end
end

# adapted from https://github.com/imathis/octopress/blob/master/Rakefile
# usage rake new_post['My New Post'] or rake new_post (defaults to "My New Post")
desc 'Start a new page'
task :newpage, :title do |_t, args|
  args.with_defaults(title: 'My New page')
  title = args.title
  filename = "#{title.downcase.gsub(/&/, 'and').gsub(/[,'":?!()\[\]]/, '').gsub(/[\W.]/, '-').gsub(/-+$/, '')}.md"
  puts "Creating new page: #{filename}"
  open(filename, 'w') do |post|
    post.puts '---'
    post.puts 'layout: page'
    post.puts "permalink: #{title.downcase.gsub(/&/, 'and').gsub(/[,'":?!()\[\]]/, '').gsub(/[\W.]/, '-').gsub(/-+$/,
                                                                                                               '')}/index.html"
    post.puts "title: \"#{title.gsub(/&/, '&amp;')}\""
    post.puts 'description: '
    post.puts 'headline: '
    post.puts "modified: #{Time.now}"
    post.puts 'tags: []'
    post.puts 'image: '
    post.puts '  feature: '
    post.puts 'comments: true'
    post.puts 'mathjax: '
    post.puts '---'
  end
end

desc '提交文章'
task :post do
  exec 'git add .'
  exec "git commit -m 'publish'"
  exec 'git push'
  puts '完成..'
end
