const { execSync } = require('child_process')

const shell = cmd => execSync(cmd, { cwd: '/tmp', encoding: 'utf8', stdio: 'inherit' })

exports.lambdaHandler = async (event, context) => {
  shell('git clone --depth 1 https://github.com/lambci/yumda')

  shell('gm convert ./yumda/examples/sam_squirrel.jpg -negate -contrast -resize 100x100 thumbnail.jpg')

  // Normally we'd perhaps upload to S3, etc... but here we just convert to ASCII:

  shell('jp2a --width=69 thumbnail.jpg')
}
