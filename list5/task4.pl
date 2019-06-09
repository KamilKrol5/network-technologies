  use HTTP::Daemon;
  use HTTP::Status;  
  #use IO::File;

  my $d = HTTP::Daemon->new(
           LocalAddr => 'localhost',
           LocalPort => 4321,
       )|| die;
  
  print "Please contact me at: <URL:", $d->url, ">\n";


  while (my $c = $d->accept) {
      while (my $r = $c->get_request) {
          if ($r->method eq 'GET') {
            print "HEADERS: \n";
            print $r->headers_as_string;

            $response = HTTP::Response->new();
            $response->content($r->headers_as_string);
            print "RESPONSE: \n";
            print $response->as_string;
            $c->send_response($response);
          }
          else {
              $c->send_error(RC_FORBIDDEN)
          }

      }
      $c->close;
      undef($c);
  }