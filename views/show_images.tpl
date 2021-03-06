%include header name=name
%include sidebar is_admin=is_admin

        <div class="span9">
        %if images:
          <table class="table table-striped table-bordered table-condensed">
            <thead>
              <tr>
                <th colspan="2">Images</th>
              </tr>
              <tr>
                <th>Name</th>
                <th>Type</th>
                <th>Services</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
                %for i in images:
                <tr>
                  <td>{{i.name}}</td>
                  <td>{{i.imagetypes.name}}</td>
                  <td>
                    %for service in i.imagetypes.services:
                      {{service.name}}<br />
                    %end # for service in imagetypes.services
                  </td>

                  <td>{{i.description}}</td>
                </tr>
                %end # for i in images
            </tbody>
          </table>
          %else: 
          <div class="alert">
             You are not registered in any classes 
          </div>
          %end #if images
        
          </div><!--/row-->
        </div><!--/span-->
%include footer