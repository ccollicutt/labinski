%include header
%include sidebar
        <div class="span9">
          <table class="table table-striped table-bordered table-condensed">
            <thead>
              <tr>
                <th colspan="2">Connections</th>
              </tr>
              <tr>
                <th>Instance</th>
                <th>Type</th>
                <th>SSH Command</th>
                <th>Password</th>
              </tr>
            </thead>
            <tbody>
              %for server in servers:
              <tr>
                <td><a href="/someurl"><a href="{{server.get_vnc_console('novnc')['console']['url']}}" target="_blank">Matlab</a></td>
                <td>Linux</td>
                <td>ssh -p 2222 admin@{{server.addresses['private'][0]['addr']}}</td>
                <td>superpownuclearbuttoncar</td>
              <tr>
              %end #for server in servers
            </tbody>
          </table>
        
          </div><!--/row-->
        </div><!--/span-->
%include footer