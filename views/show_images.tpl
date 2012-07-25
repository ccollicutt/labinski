%include header
%include sidebar
        <div class="span9">
        %if classes:
          <table class="table table-striped table-bordered table-condensed">
            <thead>
              <tr>
                <th colspan="2">Images</th>
              </tr>
              <tr>
                <th>Name</th>
                <th>Type</th>
                <th>Description</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              %for c in classes:
                %for i in c.images:
                <tr>
                  <td>{{i.name}}</td>
                  <td>{{i.image_type.name}}</td>
                  <td>{{i.description}}</td>
                  <td><a class="btn" href="/reserve/{{i.os_image_id}}/{{i.name}}">Reserve</a></td>
                </tr>
                %end # for i c.images
              %end # for c in classes
            </tbody>
          </table>
          %else: 
          <div class="alert">
             You are not registered in any classes 
          </div>
          %end #if classes
        
          </div><!--/row-->
        </div><!--/span-->
%include footer