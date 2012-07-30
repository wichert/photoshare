var UploadItem = Backbone.Model.extend({
    defaults: {
          file: null,
          progress: 0,
          status: "upload"
    },

    _makeXHR: function() {
        var xhr = new XMLHttpRequest(),
            model = this.context;
        xhr.upload.addEventListener("progress", _.bind(model.onProgress, model), false);
        return xhr;
    },

    upload: function() {
        var data = new FormData();
        data.append("file", this.get("file"));
        $.ajax(upload_url, {
            type: "POST",
            context: this,
            xhr: this._makeXHR,
            data: data,
            processData: false,
            dataType: "json",
            error: this.onError,
            success: this.onSuccess
        });
    },

    onError: function(jqXHR, textStatus, errorThrown) {
        console.log("An error occured during upload.");
        this.set({status: "error"});
    },

    onSuccess: function(data, textStatus, jqXHR) {
        console.log("Upload completed succesfully.");
        this.set({status: "complete"});
    },

    onProgress: function(event) {
        this.set({progress: (event.loaded / event.total)*100});
    }
});

var UploadQueue = Backbone.Collection.extend({
    model: UploadItem,
});


var ActiveUploads = new UploadQueue;

var UploadItemView = Backbone.View.extend({
    tagName: "li",

    template: _.template($("#uploaditem-template").html()),

    initialize: function() {
        this.model.bind("change", this.render, this);
        this.model.bind("destroy", this.remove, this);
    },

    prettyFilesize: function(size) {
        var units = ["bytes", "kB", "MB", "GB", "TB"], i=0;

        while (size>1024 && units[i+1]) {
            size /= 1024;
            i++;
        }
        return size.toFixed(1) + " " + units[i];
    },

    render: function() {
        var model = this.model,
            file = model.get("file");
        $(this.el).html(
            this.template({
                status: model.get("status"),
                size: this.prettyFilesize(file.size),
                name: file.name,
                progress: model.get("progress")}))
            .attr("class", model.get("status"));

        return this;
    }
});


var UploadPanelView = Backbone.View.extend({
    el: $("#upload-panel"),

    events: {
    },

    initialize: function() {
        method = _.bind(this.onDrop, this);
        $(document).on("drop", ".dropbox", method);
        $(document).on("dragenter", ".dropbox", function() {
            $(this).addClass("hover");
        }).on("dragleave", ".dropbox", function() {
            $(this).removeClass("hover");
        });
        ActiveUploads.bind("add", this.queueUpload, this);
    },

    queueUpload: function(item) {
        var view = new UploadItemView({model: item});
        this.$("#upload-queue").prepend(view.render().el);
        item.upload();

    },

    onDrop: function(event) {
        var transfer = event.originalEvent.dataTransfer, file, i, model;
        event.stopPropagation();
        event.preventDefault();
	for (i=0; i<transfer.files.length; i++) {
            file = transfer.files[i];
            if (file.name.match(/\.zip$/) !== null ||
                    file.type.match(/^image\//) !== null) {
                model = new UploadItem({file: file});
                ActiveUploads.add([model]);
            } else {
                $("<li/>", {"class": "error"}).text(
                        file.name + ": unsupported file type")
                    .prependTo($("#upload-queue"));
            }
        }
        $(".dropbox").removeClass("hover");
    }
});

/*
var PsRouter = Backbone.Router.extend({
    routes: {
        "login":  "login",
        "photos/:name": "showAlbum",
        "upload": "upload",
        "*default": "unknown"
    },


    unknown: function() {
        App.navigate("login", {trigger: true, replace: true});
    },

    login: function() {
    }
});

var Router = new PsRouter();
*/

var PsView = Backbone.View.extend({
    status: "upload",

    el: $("#content"),

    anon_template: _.template($("#app-anon-template").html()),
    auth_template: _.template($("#app-auth-template").html()),

    initialize: function() {
        this.upload_panel = new UploadPanelView;
        this.render();
/*        Router.on("route:upload", function() {
            this.status = "upload";
            this.render();
        }, this);
*/
    },

    render: function() {
	if (this.status=== "login") {
            this.$el
                .html(this.anon_template({}))
                .attr("class", "container");
        } else {
            this.$el
                .html(this.auth_template({}))
                .attr("class", "container-fluid");
        }
    }
});


var App = new PsView;
// Backbone.history.start();

