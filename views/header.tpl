
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>The Labinski</title>
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

    <!-- Le javascript
    ================================================== -->
    <script src="/bootstrap/js/jquery.js"></script>
    <script src="/bootstrap/js/bootstrap-transition.js"></script>
    <script src="/bootstrap/js/bootstrap-alert.js"></script>
    <script src="/bootstrap/js/bootstrap-modal.js"></script>
    <script src="/bootstrap/js/bootstrap-dropdown.js"></script>
    <script src="/bootstrap/js/bootstrap-scrollspy.js"></script>
    <script src="/bootstrap/js/bootstrap-tab.js"></script>
    <script src="/bootstrap/js/bootstrap-tooltip.js"></script>
    <script src="/bootstrap/js/bootstrap-popover.js"></script>
    <script src="/bootstrap/js/bootstrap-button.js"></script>
    <script src="/bootstrap/js/bootstrap-collapse.js"></script>
    <script src="/bootstrap/js/bootstrap-carousel.js"></script>
    <script src="/bootstrap/js/bootstrap-typeahead.js"></script>
    
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

          %if defined('name'):
          <div class="btn-group pull-right">
            <a class="btn dropdown-toggle" data-toggle="dropdown" href="#">
              <i class="icon-user"></i> {{name}}
              <span class="caret"></span>
            </a>
            <ul class="dropdown-menu">
              <li><a href="/">Dashboard</a></li>

              <li class="divider"></li>
              <li><a href="/logout">Sign Out</a></li>
            </ul>
          </div>
        %end

          <div class="nav-collapse">
            <ul class="nav">
              <li><a href="/">Home</a></li>
              <li><a href="/about">About</a></li>
              <li><a href="/help">Help</a></li>
            </ul>
            % if not defined('name'):
            <ul class="nav pull-right">
              <li><a href="/logout">Logout</a></li>
            </ul>
            %end
          </div><!--/.nav-collapse -->
        </div>
      </div>
    </div>

