

document.addEventListener('DOMContentLoaded', (event) => {
    const buttons = document.querySelectorAll('button');

    buttons.forEach(button => {
        button.addEventListener('mousedown', () => {
            button.classList.add('button-click-effect');
        });
        button.addEventListener('mouseup', () => {
            button.classList.remove('button-click-effect');
        });
        button.addEventListener('mouseleave', () => {
            button.classList.remove('button-click-effect');
        });
    });
});

document.addEventListener('DOMContentLoaded', (event) => {
    const containers = document.querySelectorAll('.container');

    containers.forEach(container => {
        container.addEventListener('mouseenter', () => {
            container.classList.add('pulse');
        });

        container.addEventListener('mouseleave', () => {
            container.classList.remove('pulse');
        });
    });
});
