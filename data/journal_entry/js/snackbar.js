/**
 * menu.snackbar.js
 * menu.snackbar module
 * 
 * designed by SAMBUICHI, Nobuyuki (Sambuichi Professional Engineers Office)
 * written by SAMBUICHI, Nobuyuki (Sambuichi Professional Engineers Office)
 * 
 * MIT License
 * 
 * (c) 2023 SAMBUICHI Nobuyuki (Sambuichi Professional Engineers Office)
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */
snackbar = (function () {

    function open(param) { // param: { message, type }
        const snackbarEl = document.getElementById('snackbar');
        const type = param.type;
        const timeout = 3000;
        let message = param.message;
        message = message.trim();
        // message = wuwei.nls.translate(message);
        if (message.length > 128) {
            message = message.substr(0, 128) + '...';
        }
        snackbarEl.innerHTML = message;
        snackbarEl.className = 'show bg-' + type;
        /**
         * Bootstrap 4 Colors
         * bg-success bg-info bg-warning bg-danger bg-secondary bg-dark bg-light
         * text white text-dark
         */
        if (['warning', 'light', 'white', 'transparent'].indexOf(type) >= 0) {
            snackbarEl.style.color = '#303030';
        } else {
            /** primary secondary success info danger dark */
            snackbarEl.style.color = '#efefef';
        }
        setTimeout(() => {
            close();
        }, timeout);
        snackbarEl.classList.remove('hidden');
    }

    function close() {
        const snackbarEl = document.getElementById('snackbar');
        snackbarEl.innerHTML = '';
        snackbarEl.className = '';
    }

    return {
        open: open,
        close: close
    };
})();
