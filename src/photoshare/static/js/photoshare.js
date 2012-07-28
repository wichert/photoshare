var UploadItem = Backbone.Model.extend({
    defaults: {
          file: null,
          progress: 0,
          status: "upload"
    },

    upload: function() {
        var data = new FormData(),
            req = new XMLHttpRequest();
        data.append("file", this.get("file"));
        req.addEventListener("error", _.bind(this.onError, this), false);
        req.addEventListener("progress", _.bind(this.onProgress, this), false);
        req.addEventListener("load", _.bind(this.onComplete, this), false);
        req.open("POST", upload_url);
        req.send();
    },

    onError: function(event) {
        console.log("An error occured during upload.");
        this.set({status: "error"});
    },

    onComplete: function(event) {
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

var AppView = Backbone.View.extend({
    initialize: function() {
        this.upload_panel = new UploadPanelView;
    }
});

var App = new AppView;
