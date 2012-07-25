
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>hackavcl</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <!-- Le styles -->
    <link href="/bootstrap/css/bootstrap.css" rel="stylesheet">
    <style type="text/css">
      body {
        padding-top: 60px;
        padding-bottom: 40px;
      }
      .sidebar-nav {
        padding: 9px 0;
      }
    </style>
    <link href="/bootstrap/css/bootstrap-responsive.css" rel="stylesheet">

    <!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->

    <!-- Le fav and touch icons -->
    <link rel="shortcut icon" href="/bootstrap/ico/favicon.ico">
    <link rel="apple-touch-icon-precomposed" sizes="144x144" href="/bootstrap/ico/apple-touch-icon-144-precomposed.png">
    <link rel="apple-touch-icon-precomposed" sizes="114x114" href="/bootstrap/ico/apple-touch-icon-114-precomposed.png">
    <link rel="apple-touch-icon-precomposed" sizes="72x72" href="/bootstrap/ico/apple-touch-icon-72-precomposed.png">
    <link rel="apple-touch-icon-precomposed" href="/bootstrap/ico/apple-touch-icon-57-precomposed.png">
  </head>

  <body>

    <div class="navbar navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container-fluid">
          <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </a>
          <a class="brand" href="/">The Labinski</a>
        
          </div><!--/.nav-collapse -->
        </div>
      </div>
    </div>
<div class="container">
    <div class="row">
        <div class="offset4 span3">
        	% if defined('error_msg'):
        	<div class="alert alert-error">
				{{error_msg}}
			</div>
			% end
            <form class="form-horizontal" method="post" action="/login">
                <fieldset>
                    <legend>Please login</legend>
                    <div class="control-group">
                        <label class="control-label" for="name">Username</label>
                        <div class="controls">
                            <input name="name" maxlength="100" type="text" class="input-large" id="name" />
                        </div>
                    </div>
                    <div class="control-group">
                        <label class="control-label" for="password">Password</label>
                        <div class="controls">
                            <input name="password" maxlength="100" type="password" class="input-large" id="password" />
                        </div>
                    </div>
                        <div class="form-actions">
           					<button type="submit" class="btn btn-primary">Login</button>
          				</div>
                </fieldset>
            </form>
        </div>
    </div>
</div>

%include footer