// Three.js 3D Background Animation
// Advanced 3D Expense Tracker - Cyberpunk Particle System

(function() {
    const canvas = document.getElementById('threejs-bg');
    if (!canvas) return;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });

    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setClearColor(0x000000, 0);

    camera.position.z = 30;

    // === PARTICLE SYSTEM ===
    const particleCount = 800;
    const particlesGeometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);
    const sizes = new Float32Array(particleCount);

    const colorPalette = [
        new THREE.Color(0x00d4ff), // Cyan
        new THREE.Color(0xff00ff),   // Pink
        new THREE.Color(0xb829dd),  // Purple
        new THREE.Color(0x00ff88),  // Green
        new THREE.Color(0xffffff)   // White
    ];

    for (let i = 0; i < particleCount; i++) {
        const i3 = i * 3;
        positions[i3] = (Math.random() - 0.5) * 100;
        positions[i3 + 1] = (Math.random() - 0.5) * 100;
        positions[i3 + 2] = (Math.random() - 0.5) * 60;

        const color = colorPalette[Math.floor(Math.random() * colorPalette.length)];
        colors[i3] = color.r;
        colors[i3 + 1] = color.g;
        colors[i3 + 2] = color.b;

        sizes[i] = Math.random() * 2 + 0.5;
    }

    particlesGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    particlesGeometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    particlesGeometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

    const particlesMaterial = new THREE.PointsMaterial({
        size: 0.15,
        vertexColors: true,
        transparent: true,
        opacity: 0.8,
        blending: THREE.AdditiveBlending,
        sizeAttenuation: true
    });

    const particles = new THREE.Points(particlesGeometry, particlesMaterial);
    scene.add(particles);

    // === FLOATING WIREFRAME CUBES ===
    const cubes = [];
    const cubeCount = 8;

    for (let i = 0; i < cubeCount; i++) {
        const size = Math.random() * 3 + 1;
        const geometry = new THREE.BoxGeometry(size, size, size);
        const material = new THREE.MeshBasicMaterial({
            color: colorPalette[i % colorPalette.length],
            wireframe: true,
            transparent: true,
            opacity: 0.3
        });
        const cube = new THREE.Mesh(geometry, material);

        cube.position.x = (Math.random() - 0.5) * 60;
        cube.position.y = (Math.random() - 0.5) * 40;
        cube.position.z = (Math.random() - 0.5) * 30 - 10;

        cube.userData = {
            rotSpeedX: (Math.random() - 0.5) * 0.01,
            rotSpeedY: (Math.random() - 0.5) * 0.01,
            floatSpeed: Math.random() * 0.5 + 0.3,
            floatOffset: Math.random() * Math.PI * 2,
            originalY: cube.position.y
        };

        scene.add(cube);
        cubes.push(cube);
    }

    // === GRID FLOOR ===
    const gridHelper = new THREE.GridHelper(100, 50, 0x00d4ff, 0x1a1a2e);
    gridHelper.position.y = -25;
    gridHelper.material.transparent = true;
    gridHelper.material.opacity = 0.15;
    scene.add(gridHelper);

    // === MOUSE INTERACTION ===
    let mouseX = 0;
    let mouseY = 0;
    let targetMouseX = 0;
    let targetMouseY = 0;

    document.addEventListener('mousemove', (e) => {
        targetMouseX = (e.clientX / window.innerWidth - 0.5) * 2;
        targetMouseY = (e.clientY / window.innerHeight - 0.5) * 2;
    });

    // === ANIMATION LOOP ===
    let time = 0;
    let isVisible = true;

    // Visibility check
    const observer = new IntersectionObserver((entries) => {
        isVisible = entries[0].isIntersecting;
    }, { threshold: 0 });
    observer.observe(canvas);

    function animate() {
        requestAnimationFrame(animate);

        if (!isVisible) return;

        time += 0.01;

        // Smooth mouse follow
        mouseX += (targetMouseX - mouseX) * 0.05;
        mouseY += (targetMouseY - mouseY) * 0.05;

        // Camera movement based on mouse
        camera.position.x += (mouseX * 3 - camera.position.x) * 0.02;
        camera.position.y += (-mouseY * 2 - camera.position.y) * 0.02;
        camera.lookAt(0, 0, 0);

        // Animate particles
        const positions = particles.geometry.attributes.position.array;
        for (let i = 0; i < particleCount; i++) {
            const i3 = i * 3;
            positions[i3 + 1] += Math.sin(time + i * 0.1) * 0.02;
            positions[i3] += Math.cos(time * 0.5 + i * 0.05) * 0.01;
        }
        particles.geometry.attributes.position.needsUpdate = true;
        particles.rotation.y = time * 0.05;

        // Animate cubes
        cubes.forEach((cube, i) => {
            cube.rotation.x += cube.userData.rotSpeedX;
            cube.rotation.y += cube.userData.rotSpeedY;
            cube.position.y = cube.userData.originalY + 
                Math.sin(time * cube.userData.floatSpeed + cube.userData.floatOffset) * 2;

            // Pulse opacity
            cube.material.opacity = 0.2 + Math.sin(time * 2 + i) * 0.15;
        });

        // Grid animation
        gridHelper.position.z = Math.sin(time * 0.3) * 2;

        renderer.render(scene, camera);
    }

    animate();

    // === RESIZE HANDLER ===
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
})();
