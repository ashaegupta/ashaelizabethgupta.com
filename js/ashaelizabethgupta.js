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
        asha.checkHashChange(asha.loadFromHash);
    }
    asha.loadDeferredImages();
});

asha.loadProject = function() {
    /* shows the appropriate tab when the page first loads.
     */
    var project = asha.getHash();
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

asha.getHash = function () {
    return window.location.hash.substring(1);
};

asha.loadFromHash = function() {
    var project = asha.getHash();
    if (project) {
        asha.showProject(project);
    }
};

asha.checkHashChange = function(callback) {
    /* loads the appropriate project tab when the url hash changes.
     * This removes tab changing logic from links. Links just change the hash,
     * and this takes care of loading the right data
     */
    if ("onhashchange" in window) { // event supported?
        window.onhashchange = function () {
            callback();
        };
    }
    else { // event not supported:
        var storedHash = window.location.hash;
        window.setInterval(function () {
            if (window.location.hash != storedHash) {
                storedHash = window.location.hash;
                callback();
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
photos.baseUrl = 'http://ashaelizabethgupta.com/pictures/';
photos.callbackArg = '?callback=';
photos.latestCallback = photos.callbackArg + 'photos.getLatestPhotos';
photos.olderCallback = photos.callbackArg + 'photos.getOlderPhotos';
photos.newerCallback = photos.callbackArg + 'photos.getNewerPhotos';
photos.aroundCallback = photos.callbackArg + 'photos.getPhotosAround';
photos.gettingMore = false;
photos.changedOnce = false;

photos.loadPhotos = function() {
    /* when the page first loads, this gets the latest pictures
     * from the server and starts listening for keyboard shortcuts
     */
    var photoToLoad = asha.getHash();
    if (photoToLoad) {
        var url = photos.baseUrl + 'around/' + photoToLoad + photos.aroundCallback;
    } else {
        var url = photos.baseUrl + 'latest' + photos.latestCallback;
    }
    photos.loadScript(url);
    photos.bindEventsToPrevNextLink();
    photos.listenForKeyboardShortcuts();
};

photos.getAndLoadMorePhotos = function(older, newer) {
    /* gets another page of images from the server
     */
    if (older) {
        var oldest = photos.photoList[photos.photoList.length - 1].created_time;
        var next = 'http://ashaelizabethgupta.com/pictures/olderthan/' + oldest + photos.olderCallback;
    } else if (newer) {
        var newest = photos.photoList[0].created_time;
        var next = 'http://ashaelizabethgupta.com/pictures/newerthan/' + newest + photos.newerCallback;
    }
    photos.loadScript(next);
};

photos.getOlderPhotos = function(olderPhotos) {
    /* jsonp callback to display photos received from the server
     * that are older than the current one 
     * the jsonp callback methods ...*/
    photos.photoList.push.apply(photos.photoList, olderPhotos); 
    photos.currentPhoto++;
    photos.showCurrentPhoto();
    photos.gettingMore = false;
    photos.warmCache(olderPhotos);
};

photos.getNewerPhotos = function(newerPhotos) {
    /* jsonp callback to display photos received from the server
     * that are newer than the current one */
    photos.currentPhoto = newerPhotos.length;
    newerPhotos.push.apply(newerPhotos, photos.photoList); 
    photos.photoList = newerPhotos.slice(0);
    if (photos.currentPhoto > 0) {
        photos.currentPhoto--;
        photos.showCurrentPhoto();
        photos.warmCache(newerPhotos);
    }
    photos.gettingMore = false;
};

photos.getPhotosAround = function(photoList) {
    /* jsonp callback to display the photo in the hash
     * and prepare photos before and after it */
    var desiredPhoto = asha.getHash();
    photos.photoList = photoList;
    photos.currentPhoto = 0;
    for (var i=0; i<photos.photoList.length; i++) {
        if (photos.photoList[i].created_time == desiredPhoto) {
            photos.currentPhoto = i;
            break;
        }
    }
    photos.showCurrentPhoto();
    photos.warmCache(photoList);
};

photos.getLatestPhotos = function(photoList) {
    /* jsonp callback to process and display the 
     * latest pictures available */
    photos.photoList = photoList;
    photos.currentPhoto = 0;
    photos.showCurrentPhoto();
    photos.warmCache(photoList);
};

photos.warmCache = function(photoList) {
    /* loads all the images in the list of photos in 
     * hidden divs, so they are ready in the cache when we 
     * want to display them */
    for (var i=0; i<photoList.length; i++) {
        var cw = document.createElement('img');
        var src = photoList[i].images.standard_resolution.url;
        cw.setAttribute('src', src);
        var cacheWarmingHiddenDiv = document.getElementById('picture_cache_warmer');
        cacheWarmingHiddenDiv.appendChild(cw)
    }
};

photos.showCurrentPhoto = function() {
    /* swaps the currently displayed image with the 
     * image that's in the currentPhoto index in image list */
    // image
    var cp = photos.photoList[photos.currentPhoto];
    var img = document.getElementById('picture_img')
    var src = cp.images.standard_resolution.url;
    img.setAttribute('src', src);

    // caption
    var caption = document.getElementById('picture_caption')
    var text = '';
    if (cp.caption && cp.caption.text) {
        text = cp.caption.text;
    }
    caption.innerHTML = text;

    // link that the image points to
    var link = document.getElementById('picture_link');
    link.href = cp.link;

    // url hash
    window.location.hash = cp.created_time;

    photos.hideHelpText();
};

photos.hideHelpText = function() {
    /* hide the prev and next help text if the user moves to a new picture */
    var prev_help = document.getElementById('picture_prev_help');
    var next_help = document.getElementById('picture_next_help');
    var prev_link = document.getElementById('picture_prev_link');
    if (photos.changedOnce) {
        prev_help.style.color = 'white';
        prev_link.style.color = 'black';
        next_help.style.color = 'white';
    } else {
        photos.changedOnce = true;
    }
};

photos.showNextPhoto = function() {
    /* show the next photo in the stored list of photos.
     * if required, download some more from the server */
    if (photos.currentPhoto < photos.photoList.length - 1) {
        photos.currentPhoto++;
        photos.showCurrentPhoto();
    } else if (photos.currentPhoto == photos.photoList.length - 1) {
        if (!photos.gettingMore) {
            photos.gettingMore = true;
            photos.getAndLoadMorePhotos(true, false);
        }
    }
};

photos.showPreviousPhoto = function() {
    /* show the previous photo in the stored list of photos
     * if required, download some more from the server */
    if (photos.currentPhoto > 0) {
        photos.currentPhoto--;
        photos.showCurrentPhoto();
    } else if (photos.currentPhoto == 0) {
        if (!photos.gettingMore) {
            photos.gettingMore = true;
            photos.getAndLoadMorePhotos(false, true);
        }
    }
};

photos.bindEventsToPrevNextLink = function() {
    /* make the next and prev photo buttons clickable */
    var prev_link = document.getElementById('picture_prev_link');
    asha.listen(prev_link, 'click', function() {
        photos.showPreviousPhoto();
    });

    var next_link = document.getElementById('picture_next_link');
    asha.listen(next_link, 'click', function() {
        photos.showNextPhoto();
    });
};

photos.loadScript = function(_src) {
    /* makes a jsonp request for _src */
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

/* cookies */
asha.createCookie = function(name,value,days) {
    if (days) {
        var date = new Date();
        date.setTime(date.getTime()+(days*24*60*60*1000));
        var expires = "; expires="+date.toGMTString();
    }
    else var expires = "";
    document.cookie = name+"="+value+expires+"; path=/";
};

asha.readCookie = function(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
};

asha.eraseCookie = function(name) {
    createCookie(name,"",-1);
};
