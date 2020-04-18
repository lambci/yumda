# yumda – yum for Lambda

A [Linux distro](https://en.wikipedia.org/wiki/Linux_distribution) of software packages that have
been recompiled for an AWS Lambda environment, with a
[yum](https://access.redhat.com/sites/default/files/attachments/rh_yum_cheatsheet_1214_jcs_print-1.pdf)
configuration to install them (requires [Docker](https://docs.docker.com/install/)).

---

## Contents

* [Quickstart](#quickstart)
* [AWS SAM Example](#full-example-with-aws-sam)
* [Serverless Framework Example](#example-with-serverless-framework)
* [Requesting Packages to Add](#requesting-packages-to-add)
* [Building/Hosting Your Own Packages](#buildinghosting-your-own-packages)

---

## Quickstart

Usage:
```console
docker run lambci/yumda:<version> yum <yum-args>
```

For newer Amazon Linux 2 Lambda runtimes use `lambci/yumda:2`. For older runtimes (`python2.7`, `python3.6` ,`python3.7`, `ruby2.5`,
`java8`, `go1.x`, `dotnetcore2.1` or `provided`) use `lambci/yumda:1`.

Eg, to see what [packages are available for Amazon Linux 2 runtimes](https://github.com/lambci/yumda/blob/master/amazon-linux-2/packages.txt):

```console
$ docker run --rm lambci/yumda:2 yum list available

Loaded plugins: ovl, priorities
Available Packages
GraphicsMagick.x86_64        1.3.32-1.lambda2                            lambda2
GraphicsMagick-c++.x86_64    1.3.32-1.lambda2                            lambda2
ImageMagick.x86_64           6.7.8.9-15.lambda2.0.2                      lambda2
OpenEXR.x86_64               1.7.1-7.lambda2.0.2                         lambda2
OpenEXR-libs.x86_64          1.7.1-7.lambda2.0.2                         lambda2
alsa-lib.x86_64              1.1.4.1-2.lambda2                           lambda2
apr.x86_64                   1.6.3-5.lambda2.0.2                         lambda2

# etc...
```

To install a dependency (eg, `ghostscript`) into a local directory (which could be zipped up into a
[layer](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html)):

```console
$ mkdir -p gs-layer
$ docker run --rm -v "$PWD"/gs-layer:/lambda/opt lambci/yumda:2 yum install -y ghostscript

Loaded plugins: ovl, priorities
Resolving Dependencies
--> Running transaction check
---> Package ghostscript.x86_64 0:9.06-8.lambda2.0.5 will be installed
--> Processing Dependency: urw-fonts >= 1.1 for package: ghostscript-9.06-8.lambda2.0.5.x86_64
--> Processing Dependency: lcms2 >= 2.6 for package: ghostscript-9.06-8.lambda2.0.5.x86_64
--> Processing Dependency: poppler-data for package: ghostscript-9.06-8.lambda2.0.5.x86_64
--> Processing Dependency: libtiff.so.5(LIBTIFF_4.0)(64bit) for package: ghostscript-9.06-8.lambda2.0.5.x86_64
--> Processing Dependency: libpng15.so.15(PNG15_0)(64bit) for package: ghostscript-9.06-8.lambda2.0.5.x86_64

# etc...

# Then you can zip it up and publish a layer

$ cd gs-layer
$ zip -yr ../gs-layer.zip .
$ cd ..
$ aws lambda publish-layer-version --layer-name gs-layer --zip-file fileb://gs-layer.zip --description "Ghostscript Layer"
```

## Full example with [AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html)

Let's say you want to create a Lambda function that needs to clone a git repository and then manipulate an image using [GraphicsMagick](http://www.graphicsmagick.org/). For fun, we'll also convert it to ASCII art and log it.

The example we'll walk through below uses `nodejs10.x` runtime (and hence `lambci/yumda:2`). The code for this example lives in the [examples/nodejs10.x](https://github.com/lambci/yumda/tree/master/examples/nodejs10.x) directory, but we'll walk through the steps of creating it from scratch. For older runtimes, see [examples/python3.7](https://github.com/lambci/yumda/tree/master/examples/python3.7) and just replace any usage below of `lambci/yumda:2` with `lambci/yumda:1`.

Start off by creating a new SAM app:

```console
sam init --runtime nodejs10.x --name yumda-example
cd yumda-example
```

We'll edit the function code in `hello-world/app.js` to run the commands we want:

```js
const { execSync } = require('child_process')

const shell = cmd => execSync(cmd, { cwd: '/tmp', encoding: 'utf8', stdio: 'inherit' })

exports.lambdaHandler = async (event, context) => {
  shell('git clone --depth 1 https://github.com/lambci/yumda')

  shell('gm convert ./yumda/examples/sam_squirrel.jpg -negate -contrast -resize 100x100 thumbnail.jpg')

  // Normally we'd perhaps upload to S3, etc... but here we just convert to ASCII:

  shell('jp2a --width=69 thumbnail.jpg')
}
```

These binaries (`git`, `gm`, `jp2a`) don't exist on Lambda, so we'll need to install them – this is where `yumda` comes in:

```console
# Assume we're still in the yumda-example directory
mkdir -p dependencies
docker run --rm -v "$PWD"/dependencies:/lambda/opt lambci/yumda:2 yum install -y git GraphicsMagick jp2a
```

Now we have the binaries (and their dependencies) in a local directory that can be deployed as a layer alongside our function.

We can declare our layer in `template.yaml`, so the whole app looks like this:

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  HelloWorldFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: hello-world/
      Handler: app.lambdaHandler
      Runtime: nodejs10.x
      Layers:
        - !Ref DependenciesLayer

  DependenciesLayer:
    Type: AWS::Serverless::LayerVersion
    Properties:
      ContentUri: dependencies/
```

You can use the AWS SAM CLI to test it:

```console
$ sam local invoke --no-event

Invoking app.lambdaHandler (nodejs10.x)
DependenciesLayer is a local Layer in the template
Image was not found.
Building image...
Requested to skip pulling images ...

Mounting /tmp/sam-app/hello-world as /var/task:ro,delegated inside runtime container
START RequestId: 6908f297-72af-143f-dd79-2b6128c5c428 Version: $LATEST
Cloning into 'yumda'...
                             ....'',,,''....                         
                      .';codddddddddddddddddddol;'.                  
                  .,ldxdddddddddddddddddodddooddddolc;.              
               .codddddoddddddddddddddddddddddddddddolllc'           
            .;odddddddddddddddddddddddddddddddddddddddollll:.        
           :doddddddddddddddddddddddddddddddddddddoddddolooodc       
         'ddodooooddddoooddddddddddddddddddddddddddddddddlldlod'     
        cddodxkOOOOOOOOOxdddddddddddddddddddddddoddddddddooloood:    
       :ddxO00OOOOOO0OOO0Oxdddddoddddddddoddoddoodddddddddooooooxl   
      ,xxk00OOO00OOOOO0OOO0OdoxdxoclllllllddddddddodddddddoooooooO;  
      dOKkdoodk0OOO00OOOO00Oko:c:,..''.'.';ccldddddddddddddooooookO  
     .O:.      .lO0k00O0kc,::;,''''''''.''''',;;';lodddddddooooodkK' 
                 '0OOOk:'....'',,.'.'''.''',,''....'cddodddoloood0K; 
                  oKx:''....','','''.,.''''',,''. .'',ldddooooookOK: 
                  ld;'.'.,:;'',,''.,0Wx.'''',,,,;;'.''':oddoooox0OK; 
                 'o;,';:;;,,,,,,'''.okNx..'',,,,,,;:;,,;:oolood00kK. 
                .x:;;;;',''',,''''.oWclNO,.'',',''',;;;;;lloodO0O0d  
               :0x;;;;,'''',,,,,''.:,'',;'',,;,,'''',;;;;:oodOO0kK.  
             .x00d;;;:;;::::::::;c::c::c:::::c:::::::;;;;:lkOOOOK;   
           .l0OO0x;;::;;,,,,,,,,,,,,,,',,,,,,',,,,,,;;::;cOOO0kKc    
          ;O0O0OOdol.''..''...''...''''.'...''....''..',xx0O0O0:     
        .x0OOOkdodO''..'.,;:;;;;;,..''...';:;;;;;;'..''.d00k0k'      
       cKO00kxoddxd..'.':'.       ..'..'..       .;,'...:0OKl        
     .d0O0kddodddkl.'.'.            ...            ..''.;0l.         
    .OO0OxodddddoOl''..   .  ;l.     ..     .l:     ..'..            
   .O0Oxoddddddddxx'.'.    .0WWN.          lXWWc     .''             
   xOOdooddddddodkl.''. .   'od'           .cd:     ..''.    . x,x   
  ;Kxodddddddood',......    .  .  ........         ......    'lkOlo. 
  Oxoddddoddoddl   .             ..,'..,'.                           
 'Ododdddodddxxl.    .             .':;..                      .     
 :kooddddddddodk;   .            ..      ..                   ..     
 :ddddddodddddddxd.   .         .........'..                 ...     
 :xdddddddddddddddxxo.    .       ...'...       .          ......    
 'kodddddddddddddddx'   ..''...................'.'.   . ........     
 .dddodddddddddddoxl   ...'...'...'....'''''......''............     
  ,ddododdddddddddx:  ......'''....      ....''.'..'..........       
   cxoxooddddddddddo ..........              ...'..''....'..         
    cxlxdddddddododdc..........    . .        ...''..'''.            
     :xdoodddddddxll:............ .:x.          ..'..'..             
      .okxdddddd:............... .OXlx;          .'.......           
        .okOxxx,.........'.      .O;x.           .'.........         
           ;xOd..........'.       .              ...........         
             .'.............       .            ............         
               ..............                 ..............         
                ...........''.               ..'...........          
                 ...........''.....      ....'............           
                   ..........''.''........''''..........             
                     ......'...''''''''''''.''........               
                     ...'..'..               ..'..''..               
                                                                     
END RequestId: 6908f297-72af-143f-dd79-2b6128c5c428
REPORT RequestId: 6908f297-72af-143f-dd79-2b6128c5c428	Duration: 530.74 ms	Billed Duration: 600 ms	Memory Size: 128 MB	Max Memory Used: 41 MB	
null
```

### Packaging and deploying

To package and deploy our Lambda, we can also use `sam`, but there's currently [a bug packaging any layers that contain symlinks](https://github.com/awslabs/aws-sam-cli/issues/477).

You can work around that by creating the layer zip yourself:

```console
cd dependencies
zip -yr ../dependencies.zip .
cd ..
```

And then change the `ContentUri` in your `template.yaml` from `dependencies/` to `dependencies.zip`:

```yaml
# ...
  DependenciesLayer:
    Type: AWS::Serverless::LayerVersion
    Properties:
      ContentUri: dependencies.zip
```

Then you can run `sam package` (assuming you've created an S3 bucket to save your SAM artifacts to):

```console
sam package --output-template packaged.yaml --s3-bucket <sam-bucket>
```

And then you can deploy:

```console
sam deploy --template-file packaged.yaml --stack-name yumda-example --capabilities CAPABILITY_IAM
```

(your Lambda function will be named `yumda-example-HelloWorldFunction-<suffix>` if you want to invoke it via the AWS CLI or web console)

## Example with [Serverless Framework](https://serverless.com/)

We'll use the same code layout as in the example above, which you can find in the [example](https://github.com/lambci/yumda/tree/master/example) directory.

So our lambda function code lives in `./hello-world/app.js` and our dependencies are in `./dependencies`.

Our `serverless.yaml` looks like this:

```yaml
service: yumda-example

provider:
  name: aws
  runtime: nodejs10.x

package:
  individually: true
  exclude:
    - ./**

functions:
  hello-world:
    handler: hello-world/app.lambdaHandler
    package:
      include:
        - hello-world/**
    layers:
      - {Ref: DependenciesLambdaLayer}

layers:
  dependencies:
    path: dependencies
    package:
      artifact: dependencies.zip # Needed until https://github.com/serverless/serverless/issues/6580 is fixed
```

We install the dependencies the same way as in the previous example, using `yumda`:

```console
# Assume we're still in the yumda-example directory
mkdir -p dependencies
docker run --rm -v "$PWD"/dependencies:/lambda/opt lambci/yumda:2 yum install -y git GraphicsMagick jp2a
```

And then we can test this out locally:

```console
sls invoke local --docker -f hello-world
```

### Packaging and deploying

Unfortunately the Serverless Framework also has [bugs packaging up layers that have symlinks](https://github.com/serverless/serverless/issues/6580), so we'll need to zip up the dependencies ourselves to deploy them.

```
cd dependencies
zip -yr ../dependencies.zip .
cd ..
```

Then we can deploy:

```console
sls deploy
```

## Requesting Packages to Add

Please file a GitHub Issue with your request and add the `package suggestion` label. For now we'll only be considering additions that already exist in the Amazon Linux core repositories, or the `amazon-linux-extras` repositories (including `epel`).

## Building/Hosting Your Own Packages

More words are needed here...

For now, you can see all the `.spec` files for the compiled RPM packages in the [specs/lambda2](https://github.com/lambci/yumda/tree/master/amazon-linux-2/build/specs/lambda2) directory – and compare them with the corresponding [specs/amzn2](https://github.com/lambci/yumda/tree/master/amazon-linux-2/build/specs/amzn2) files to see what's been modified to get them running for a Lambda environment, as an inspiration to build your own.

The build image uses a set of [`rpmmacros`](https://github.com/lambci/yumda/blob/master/amazon-linux-2/build/rpmmacros) so the software is compiled for a `/opt` environment (as well as using `lib` instead of `lib64` as the library path).
