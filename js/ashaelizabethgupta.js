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
    asha.loadProject();
    asha.checkHashChange();
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
