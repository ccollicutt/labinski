%include header    
        <div class="span9">
          <table class="table table-striped table-bordered table-condensed">
            <thead>
              <tr>
                <th colspan="2">Reservation Schedule</th>
              </tr>
              <tr>
                <th style="width: 15%">Start Time</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
 			% for i in range(24):
 			<tr>
 				<td>{{i}}:00</td>
 				<td>
                  <div class="btn-group">
                    <button class="btn  dropdown-toggle" data-toggle="dropdown">Reserve<span class="caret"></span></button>
                    <ul class="dropdown-menu">
                      <li><a href="/reserve">matlab fake</a></li>
                      <li><a href="/reserve">other image fake</a></li>

                    </ul>
                  </div><!-- /btn-group -->
 				</td>
 			</tr>
 			%end # for i in range
            </tbody>
          </table>
        
          </div><!--/row-->
        </div><!--/span-->
%include footer