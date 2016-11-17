#
# modified with the help of Github:
# https://help.github.com/articles/deploying-with-capistrano
#
# and http://git.io/kcrfgQ
# by Shreyans Bhansali, 19 April 2014
#

default_run_options[:pty] = true
ssh_options[:forward_agent] = true
set :normalize_asset_timestamps, false

set :application,   "asha.nyc"
set :application_path, "/#{application}"

set :user, "ubuntu"
set :use_sudo, false

set :scm, :git
set :repository,    "git@github.com:ashaegupta/ashaelizabethgupta.com.git"
set :branch,        "master"
set :deploy_via,    :remote_cache

role :web,        "s1.shreyans.org"


### setup
before "deploy:setup", "asha:pre_setup"
after "deploy:setup", "deploy:update", "asha:post_setup"

### deploy
after "deploy:restart", "deploy:cleanup"

namespace :deploy do
    task :cold do
        update
    end
end

namespace :asha do
    #
    # setup
    #

    task :pre_setup do
        asha.create_symlink_to_u
    end

    task :post_setup  do
        asha.create_symlink_to_apps
    end

    desc "creates the folders that the our apps will be stored in, on instance store"
    task :create_symlink_to_u do
        run "sudo mkdir -p /mnt/u"
        run "sudo chown -R #{user}:#{user} /mnt/u"
    end

    desc "creates symlinks to our apps from /"
    task :create_symlink_to_apps do
        run "sudo ln -s #{current_path} #{application_path}"
        run "sudo chown -h #{user}:#{user} #{application_path}"
    end

end
