%include header

<div class="container">
    <div class="row">
        <div class="span12">
            <form class="form-horizontal" method="post" action="/form/">
                <fieldset>
                    <legend>Please login</legend>
                    <div class="control-group">
                        <label class="control-label" for="id_username">Username</label>
                        <div class="controls">
                            <input name="username" maxlength="100" placeholder="Enter your username..." type="text" class="input-large" id="id_username" />
                        </div>
                    </div>
                    <div class="control-group">
                        <label class="control-label" for="id_password">Password</label>
                        <div class="controls">
                            <input name="password" maxlength="100" placeholder="Enter your password..." type="password" class="input-large" id="id_password" />
                        </div>
                    </div>
                </fieldset>
            </form>
        </div>
    </div>
</div>

%include footer