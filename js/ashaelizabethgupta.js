var asha = asha || {};
asha.default_project = 'product';

asha.listen = function(el, evnt, func) {
    /* adds event listeners and deals with IE being different
     */
    if (el.addEventListener)  {// W3C DOM 
        el.addEventListener(evnt,func,false);
    } else if (el.attachEvent) { // IE DOM
         var r = el.attachEvent("on"+evnt, func);
         return r;
    }
};

asha.listen(window, 'load', function() {
    if (window.location.pathname.indexOf('pictures') != -1) {
        photos.loadPhotos();
    } else {
        asha.loadProject();
        asha.checkHashChange();
    }
    asha.loadDeferredImages();
});

asha.loadProject = function() {
    /* shows the appropriate tab when the page first loads.
     */
    var project = asha.getProjectNameFromHash();
    if (project) {
        asha.showProject(project);
    } else {
        asha.showProject(asha.default_project);
    }
}

asha.showProject = function(project) {
    /* logic associated with switching tabs
     */

    // hide all project_list classes and all category highlights
    var all_p = document.getElementsByClassName('project_list');
    for (var i=0; i<all_p.length; i++) {
        all_p[i].style.display = "none";
    }
    var all_c = document.getElementsByClassName('project_category_purple_bar');
    for (var i=0; i<all_c.length; i++) {
        all_c[i].style.display = "none";
    }
    // show the div with given id, and highlight the category
    var p_el = document.getElementById(project+"_list");
    if (p_el) {
        p_el.style.display = "inline";
    }
    var p_el = document.getElementById(project+"_purple");
    if (p_el) {
        p_el.style.display = "block";
    }
};

asha.getProjectNameFromHash = function () {
    return window.location.hash.substring(1);
};

asha.checkHashChange = function() {
    /* loads the appropriate project tab when the url hash changes.
     * This removes tab changing logic from links. Links just change the hash,
     * and this takes care of loading the right data
     */
    if ("onhashchange" in window) { // event supported?
        window.onhashchange = function () {
            var project = asha.getProjectNameFromHash();
            if (project) {
                asha.showProject(project);
            }
        };
    }
    else { // event not supported:
        var storedHash = window.location.hash;
        window.setInterval(function () {
            if (window.location.hash != storedHash) {
                storedHash = window.location.hash;
                var project = asha.getProjectNumberFromHash();
                if (project) {
                    asha.showProject(project);
                }
            }
        }, 100);
    }
};

asha.loadDeferredImages = function() {
    /* loads deferred images by finding all img tags, 
     * taking the values of their longdesc attributes,
     * and creating a src attribute with that value.
     * This allows all the html of the page to render before 
     * images have been downloaded
     */
    var images = document.getElementsByTagName('img');
    var el = null;
    var src = null;
    for (var i = 0; i < images.length; i++) {
        el = images[i];
        src = el.getAttribute('longdesc');
        if (src) {
            el.setAttribute('longdesc', '');
            el.setAttribute('src', src);
            el.setAttribute('deferred_pic_loaded', 'true');
        }
    }
};

// ********* photos *********
// code for the photos slideshow
var photos = photos || {};
photos.currentPhoto = 0;
photos.photoList = null;
photos.callbackArg = '?callback=';
photos.latestCallback = photos.callbackArg + 'photos.getLatestPhotos';
photos.moreCallback = photos.callbackArg + 'photos.getMorePhotos';
photos.gettingMore = false;

photos.loadPhotos = function() {
    var latest_url = 'http://127.0.0.1:5000/pictures/latest' + photos.latestCallback;
    photos.loadScript(latest_url);
    photos.listenForKeyboardShortcuts();
};

photos.getAndLoadMorePhotos = function() {
    // what's the latest id we've got?
    var oldest = photos.photoList[photos.photoList.length - 1].created_time;
    var next = 'http://127.0.0.1:5000/pictures/olderthan/' + oldest + photos.moreCallback;
    photos.loadScript(next);
};

photos.getMorePhotos = function(morePhotos) {
    console.log('got more');
    photos.photoList.push.apply(photos.photoList, morePhotos); 
    photos.currentPhoto++;
    photos.showCurrentPhoto();
    photos.gettingMore = false;
};

photos.getLatestPhotos = function(photoList) {
    console.log('got latest');
    photos.photoList = photoList;
    photos.currentPhoto = 0;
    photos.showCurrentPhoto();
};

photos.showCurrentPhoto = function() {
    var cp = photos.photoList[photos.currentPhoto];
    var img = document.getElementById('image')
    var src = cp.images.standard_resolution.url;
    img.setAttribute('src', src);

    var caption = document.getElementById('caption')
    var text = '';
    if (cp.caption && cp.caption.text) {
        text = cp.caption.text;
    } else {
        text = '';
    }
    caption.innerHTML = text;

    var link = document.getElementById('image_link');
    link.href = cp.link;
};

photos.loadScript = function(_src) {
    console.log('fetching '+ _src);
    var e = document.createElement('script');
    e.setAttribute('language','javascript'); 
    e.setAttribute('type', 'text/javascript');
    e.setAttribute('src',_src); 
    var parent = document.head || document.body;
    parent.appendChild(e); 
};

photos.listenForKeyboardShortcuts = function() {
    document.addEventListener('keydown', function(e) {
        // we're trying to identify the element for which this event was fired, 
        // and then decide whether or not to set off the shortcut
        // see: http://www.quirksmode.org/js/events_properties.html
        var element;
        if (e.target) element = e.target;
        else if (e.srcElement) element = e.srcElement;
        if (element.nodeType==3) element = element.parentNode;

        // don't want to set the shortcut off when you're editing text on the page
        if (element.tagName == 'INPUT' || element.tagName == 'TEXTAREA') return;

        if (e.keyCode) {
            // want to prevent these from running if the crtl, alt, shift 
            // or command keys are pressed
            if (e.ctrlKey || e.altKey || e.shiftKey || e.metaKey) return;

            if (e.keyCode == 74 || e.keyCode == 39 || e.keyCode == 40) {
                // j, right, down
                photos.showNextPhoto();
            } else if (e.keyCode == 75 || e.keyCode == 37 || e.keyCode == 38) {
                // k, left, up
                photos.showPreviousPhoto();
            }
        }
    });
};

photos.showNextPhoto = function() {
    if (photos.currentPhoto < photos.photoList.length - 1) {
        photos.currentPhoto++;
        photos.showCurrentPhoto();
    } else if (photos.currentPhoto == photos.photoList.length - 1) {
        if (!photos.gettingMore) {
            photos.gettingMore = true;
            photos.getAndLoadMorePhotos();
        }
    }
};

photos.showPreviousPhoto = function() {
    if (photos.currentPhoto > 0) {
        photos.currentPhoto--;
        photos.showCurrentPhoto();
    }
};
