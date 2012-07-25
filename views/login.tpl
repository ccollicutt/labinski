%include header

<div class="container">
    <div class="row">
        <div class="offset4 span3">
        	% if defined('error_msg'):
        	<div class="alert alert-error">
				{{error_msg}}
			</div>
			% end
            <form class="form-horizontal" method="post" action="/login">
                <fieldset>
                    <legend>Please login</legend>
                    <div class="control-group">
                        <label class="control-label" for="name">Username</label>
                        <div class="controls">
                            <input name="name" maxlength="100" type="text" class="input-large" id="name" />
                        </div>
                    </div>
                    <div class="control-group">
                        <label class="control-label" for="password">Password</label>
                        <div class="controls">
                            <input name="password" maxlength="100" type="password" class="input-large" id="password" />
                        </div>
                    </div>
                        <div class="form-actions">
           					<button type="submit" class="btn btn-primary">Login</button>
          				</div>
                </fieldset>
            </form>
        </div>
    </div>
</div>

%include footer