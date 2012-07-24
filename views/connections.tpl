%include header
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
                <td><a href="/someurl"><a href="{{server.get_vnc_console('novnc')['console']['url']}}">Matlab</a></td>
                <td>Linux</td>
                <td>ssh -p 2222 admin@10.0.4.5</td>
                <td>superpownuclearbuttoncar</td>
              <tr>
              %end #for server in servers
            </tbody>
          </table>
        
          </div><!--/row-->
        </div><!--/span-->
%include footer