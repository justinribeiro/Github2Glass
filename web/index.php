<?php
/*
* Copyright (C) 2013 Google Inc.
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*      http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/
//  Author: Jenny Murphy - http://google.com/+JennyMurphy

/*
*	This was based on the starter project; it has only one purpose; to 
*	grab some auth and dump them into the SQLite DB.
*
*	Author: Justin Ribeiro - http://justinribeiro.com
*/

require_once 'config.php';
require_once 'mirror-client.php';
require_once 'google-api-php-client/src/Google_Client.php';
require_once 'google-api-php-client/src/contrib/Google_MirrorService.php';
require_once 'util.php';

$client = get_google_api_client();

// Authenticate if we're not already
if (!isset($_SESSION['userid']) || get_credentials($_SESSION['userid']) == null) {
  header('Location: ' . $base_url . '/oauth2callback.php');
  exit;
} else {
  $client->setAccessToken(get_credentials($_SESSION['userid']));
}

// A glass service for interacting with the Mirror API
$mirror_service = new Google_MirrorService($client);

?>
<!doctype html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Github 2 Glass</title>
  <link href="./static/bootstrap/css/bootstrap.min.css" rel="stylesheet" media="screen">
  <style>
    .button-icon { max-width: 75px; }
    .tile {
      border-left: 1px solid #444;
      padding: 5px;
      list-style: none;
    }
    .btn { width: 100%; }
  </style>
</head>
<body>
<div class="navbar navbar-inverse navbar-fixed-top">
  <div class="navbar-inner">
    <div class="container">
      <a class="brand" href="#">Github 2 Glass</a>
      <div class="nav-collapse collapse">
        <form class="navbar-form pull-right" action="signout.php" method="post">
          <button type="submit" class="btn">Sign out</button>
        </form>
      </div>
    </div>
  </div>
</div>

<div class="container">
	<div class="hero-unit">
		<h1>You've signed in!</h1>
		<p>Looks like you got some auth tokens! Yippee!</p>
	</div>
  
	<div class="row-fluid">
		<div class="span12">
			<h2>Now what?</h2>
			<p>You need to fire up the background listener. To do so, work that command line:</p>
			
			<h3>Log into the virtual machine instance</h3>
			<p>Head into the project root where you started the VM, and secure shell to the instance via:</p>
			<code>$ vagrant ssh</code>
			
			<h3>Start the listener</h3>
			<p>Once you've connected, fire up the script:</p>
			<code>vagrant@precise64:~$ python /vagrant/backend/broker_listener.py</code>
			<br/><br/> <!-- <<< that there is just blah Justin....BLAH -->
			<p>Note, the listener will run with debug so you can see what's happening. It's very barebones.</p>
		</div>
	</div>
</div>

<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
<script src="/static/bootstrap/js/bootstrap.min.js"></script>
</body>
</html>
