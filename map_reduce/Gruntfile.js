module.exports = function (grunt) {
  grunt
    .initConfig({
      "couch-compile": {
        dbs: {
          files: {
            "/tmp/mastodon_policy.json": "mastodon_policy/policy_count"
          }
        }
      },
      "couch-push": {
        options: {
          user: process.env.user,
          pass: process.env.pass
        },
        mastodon_policy: {
        }
      }
    });

  grunt.config.set(`couch-push.mastodon_policy.files.http://172\\.26\\.128\\.252:5984/${process.env.dbname1}`, "/tmp/mastodon_policy.json");
  console.log(JSON.stringify(grunt.config.get()));
  grunt.loadNpmTasks("grunt-couch");
};
