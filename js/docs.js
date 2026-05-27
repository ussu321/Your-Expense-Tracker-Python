// Documentation Page JavaScript
// Advanced 3D Expense Tracker

document.addEventListener('DOMContentLoaded', function() {

    // ===== DOCS SIDEBAR ACTIVE LINK TRACKING =====
    const sections = document.querySelectorAll('.docs-section[id]');
    const navLinks = document.querySelectorAll('.docs-link');

    function updateActiveLink() {
        let current = '';
        const scrollPos = window.pageYOffset + 150;

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + current) {
                link.classList.add('active');
            }
        });
    }

    window.addEventListener('scroll', updateActiveLink);
    updateActiveLink();

    // ===== COPY CODE FUNCTION =====
    window.copyCode = function(btn) {
        const codeBlock = btn.closest('.docs-code-block').querySelector('code');
        const text = codeBlock.textContent;

        navigator.clipboard.writeText(text).then(() => {
            const originalIcon = btn.innerHTML;
            btn.innerHTML = '<i class="fas fa-check"></i>';
            btn.style.color = '#00ff88';

            setTimeout(() => {
                btn.innerHTML = originalIcon;
                btn.style.color = '';
            }, 2000);
        }).catch(err => {
            console.error('Failed to copy:', err);
        });
    };

    // ===== SMOOTH SCROLL FOR DOCS LINKS =====
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // ===== CODE SYNTAX HIGHLIGHTING (Basic) =====
    document.querySelectorAll('.docs-code-block code').forEach(block => {
        let html = block.innerHTML;

        // Highlight comments
        html = html.replace(/(#.*$)/gm, '<span style="color: #6a9955;">$1</span>');
        html = html.replace(/(\/\/.*$)/gm, '<span style="color: #6a9955;">$1</span>');

        // Highlight strings
        html = html.replace(/(".*?")/g, '<span style="color: #ce9178;">$1</span>');
        html = html.replace(/('.*?')/g, '<span style="color: #ce9178;">$1</span>');

        // Highlight keywords
        const keywords = ['git', 'python', 'pip', 'streamlit', 'cd', 'chmod', 'source', 'bash', 'cmd'];
        keywords.forEach(kw => {
            const regex = new RegExp('\b' + kw + '\b', 'g');
            html = html.replace(regex, '<span style="color: #569cd6;">' + kw + '</span>');
        });

        block.innerHTML = html;
    });

    // ===== PROGRESS INDICATOR =====
    const progressBar = document.createElement('div');
    progressBar.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        height: 3px;
        background: linear-gradient(90deg, #00d4ff, #ff00ff);
        z-index: 10000;
        transition: width 0.1s ease;
        box-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
    `;
    document.body.appendChild(progressBar);

    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const progress = (scrollTop / docHeight) * 100;
        progressBar.style.width = progress + '%';
    });
});
