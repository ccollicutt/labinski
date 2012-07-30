% if defined('name'):
	%include header name=name
% else:
	%include header
% end

    <div class="container-fluid">
      <div class="row-fluid">
      	
     <div class="offset4 span4">
      <div class="alert alert-warning">
        <button type="button" class="close" data-dismiss="alert">&times;</button>
        <strong>You have been logged out, but you must also shutdown your browser to complete the process</strong>
      </div>
     </div>

          </div><!--/row-->
        </div><!--/span-->

%include footer