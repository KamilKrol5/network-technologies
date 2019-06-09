  use HTTP::Daemon;
  use HTTP::Status;  
  #use IO::File;

  my $d = HTTP::Daemon->new(
           LocalAddr => '192.168.137.1',
           LocalPort => 4321,
       )|| die;
  
  print "Please contact me at: <URL:", $d->url, ">\n";


  while (my $c = $d->accept) {
      while (my $r = $c->get_request) {
            print "FILENAME:", $r->uri->as_string,"\n";
          if ($r->method eq 'GET') {
            my $arg = $r->uri->path;
            if ($arg eq "/") {
                $file_s= "./index.html";
                $c->send_file_response($file_s);
            } else {
                $file_s= "./".$arg;
                $c->send_file_response($file_s);
            }
          }
          else {
              $c->send_error(RC_FORBIDDEN)
          }

      }
      $c->close;
      undef($c);
  }