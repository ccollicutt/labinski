%include header name=name
%include sidebar is_admin=is_admin

        <div class="span9">
          %if servers:
          <table class="table table-striped table-bordered table-condensed">
            <thead>
              <tr>
                <th colspan="2">Connections</th>
              </tr>
              <tr>
                <th>Instance</th>
                <th>Type</th>
                <th>Connection Info</th>
              </tr>
            </thead>
            <tbody>
              %for server in servers:
              <tr>
                <td><a href="{{server.get_vnc_console('novnc')['console']['url']}}" target="_blank">{{server.name}}</a></td>
                <td>Linux</td>
                <td>ssh -p *someport* admin@{{server.addresses['private'][0]['addr']}}</td>

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