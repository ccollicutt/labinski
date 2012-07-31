<<<<<<< HEAD
%include header name=name
%include sidebar is_admin=is_admin
=======
%include header
%include sidebar
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823
        <div class="span9">
          %if servers:
          <table class="table table-striped table-bordered table-condensed">
            <thead>
              <tr>
                <th colspan="2">Reservations</th>
              </tr>
              <tr>
                <th>Instance</th>
                <th>Type</th>
                <th>Connection Info</th>
<<<<<<< HEAD
=======
                <th>Password</th>
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823
              </tr>
            </thead>
            <tbody>
              %for server in servers:
              <tr>
<<<<<<< HEAD
                <td><a href="{{server.get_vnc_console('novnc')['console']['url']}}" target="_blank">{{server.name}}</a></td>
                <td>Linux</td>
                <td>ssh -p *someport* admin@{{server.addresses['novanetwork_4'][0]['addr']}}</td>
=======
                <td><a href="{{server.get_vnc_console('novnc')['console']['url']}}" target="_blank">Matlab</a></td>
                <td>Linux</td>
                <td>ssh -p 2222 admin@{{server.addresses['private'][0]['addr']}}</td>
                <td>superpownuclearbuttoncar</td>
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823
              <tr>
              %end #for server in servers
            </tbody>
          </table>
          %else: 
            %if defined('reservations') and reservations:
                <div class="alert">
                  You have reservations, but the connections have not started yet, please wait a few seconds and refresh
                </div>
            %else:
             <div class="alert">
               You have no running images to connect to
            </div>
            %end #if reservations
          %end #if servers
        
          </div><!--/row-->
        </div><!--/span-->
%include footer