"""
Modulo Visualizzazione 3D - Campo Fotovoltaico Interattivo
Crea una rappresentazione tridimensionale del layout dei pannelli
"""

import streamlit as st
import streamlit.components.v1 as components
import math


def create_3d_field_visualization(params: dict) -> str:
    """
    Genera il codice HTML/JS per la visualizzazione 3D del campo fotovoltaico
    
    Args:
        params: dizionario con tutti i parametri dell'impianto
        
    Returns:
        str: codice HTML completo per il rendering 3D
    """
    
    # Estrazione parametri
    num_panels_per_row = params.get("num_panels_per_row", 5)
    num_rows = params.get("num_rows", 2)
    lato_maggiore = params.get("lato_maggiore", 2.5)
    lato_minore = params.get("lato_minore", 2.0)
    tilt = params.get("tilt_pannello", 30)
    azimuth = params.get("azimuth_pannello", 180)
    pitch_laterale = params.get("pitch_laterale", 3.0)
    carreggiata = params.get("carreggiata", 5.0)
    altezza_suolo = params.get("altezza_suolo", 1.0)
    
    # Calcolo dimensioni campo per centratura
    campo_larghezza = num_panels_per_row * pitch_laterale
    campo_profondita = num_rows * (lato_minore + carreggiata)
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ 
                margin: 0; 
                overflow: hidden; 
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
            }}
            #canvas-container {{ 
                width: 100%; 
                height: 600px; 
                position: relative;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            }}
            #info-panel {{
                position: absolute;
                top: 15px;
                left: 15px;
                background: rgba(255,255,255,0.95);
                padding: 15px 20px;
                border-radius: 10px;
                font-size: 13px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.15);
                z-index: 100;
                backdrop-filter: blur(10px);
            }}
            #info-panel h4 {{
                margin: 0 0 10px 0;
                color: #74a65b;
                font-size: 16px;
                font-weight: 600;
            }}
            #info-panel p {{
                margin: 5px 0;
                color: #333;
            }}
            .info-value {{
                font-weight: 600;
                color: #74a65b;
            }}
            #controls {{
                position: absolute;
                bottom: 15px;
                left: 15px;
                background: rgba(255,255,255,0.95);
                padding: 12px 15px;
                border-radius: 10px;
                font-size: 12px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.15);
                z-index: 100;
                backdrop-filter: blur(10px);
            }}
            #controls p {{
                margin: 3px 0;
                color: #666;
            }}
            .control-icon {{
                display: inline-block;
                width: 18px;
                text-align: center;
                color: #74a65b;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div id="canvas-container">
            <div id="info-panel">
                <h4> Layout Impianto</h4>
                <p><span class="info-value">{num_panels_per_row * num_rows}</span> pannelli totali</p>
                <p><span class="info-value">{num_panels_per_row}</span> × <span class="info-value">{num_rows}</span> (file × pannelli)</p>
                <p>Tilt: <span class="info-value">{tilt}°</span></p>
                <p>Azimuth: <span class="info-value">{azimuth}°</span></p>
            </div>
            
            <div id="controls">
                <p><span class="control-icon">🖱️</span> Trascina per ruotare</p>
                <p><span class="control-icon">🔍</span> Scroll per zoom</p>
                <p><span class="control-icon">👆</span> Tasto destro per muovere</p>
            </div>
        </div>

        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script>
            // ========== SETUP SCENA ==========
            const container = document.getElementById('canvas-container');
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0xe8f5e9);
            scene.fog = new THREE.Fog(0xe8f5e9, 50, 200);

            // Camera
            const camera = new THREE.PerspectiveCamera(
                60, 
                container.clientWidth / container.clientHeight, 
                0.1, 
                1000
            );
            camera.position.set(
                {campo_larghezza * 0.8}, 
                {campo_profondita * 0.6}, 
                {campo_larghezza * 0.8}
            );
            camera.lookAt(0, 0, 0);

            // Renderer
            const renderer = new THREE.WebGLRenderer({{ 
                antialias: true,
                alpha: true 
            }});
            renderer.setSize(container.clientWidth, container.clientHeight);
            renderer.setPixelRatio(window.devicePixelRatio);
            renderer.shadowMap.enabled = true;
            renderer.shadowMap.type = THREE.PCFSoftShadowMap;
            container.appendChild(renderer.domElement);

            // ========== LUCI ==========
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
            scene.add(ambientLight);

            const sunLight = new THREE.DirectionalLight(0xfff5e1, 0.8);
            sunLight.position.set({campo_larghezza * 2}, {campo_profondita * 3}, {campo_larghezza});
            sunLight.castShadow = true;
            sunLight.shadow.mapSize.width = 2048;
            sunLight.shadow.mapSize.height = 2048;
            sunLight.shadow.camera.near = 0.5;
            sunLight.shadow.camera.far = 500;
            sunLight.shadow.camera.left = -100;
            sunLight.shadow.camera.right = 100;
            sunLight.shadow.camera.top = 100;
            sunLight.shadow.camera.bottom = -100;
            scene.add(sunLight);

            // ========== TERRENO ==========
            const groundGeometry = new THREE.PlaneGeometry(
                {campo_larghezza * 1.5}, 
                {campo_profondita * 1.5}
            );
            const groundMaterial = new THREE.MeshLambertMaterial({{ 
                color: 0x8bc34a,
                side: THREE.DoubleSide 
            }});
            const ground = new THREE.Mesh(groundGeometry, groundMaterial);
            ground.rotation.x = -Math.PI / 2;
            ground.receiveShadow = true;
            scene.add(ground);

            // Griglia
            const gridHelper = new THREE.GridHelper(
                {campo_larghezza * 1.5}, 
                20, 
                0x74a65b, 
                0xa3c68b
            );
            gridHelper.material.opacity = 0.3;
            gridHelper.material.transparent = true;
            scene.add(gridHelper);

            // ========== CREAZIONE PANNELLI ==========
            const tiltRad = {tilt} * Math.PI / 180;
            const azimuthRad = ({azimuth} - 180) * Math.PI / 180;

            // Materiale pannelli
            const panelMaterial = new THREE.MeshPhongMaterial({{ 
                color: 0x1a237e,
                shininess: 60,
                specular: 0x4444ff,
                side: THREE.DoubleSide
            }});

            // Materiale frame
            const frameMaterial = new THREE.MeshStandardMaterial({{ 
                color: 0x424242,
                metalness: 0.6,
                roughness: 0.4
            }});

            // Funzione per creare un singolo pannello
            function createPanel(x, z) {{
                const panelGroup = new THREE.Group();

                // Superficie del pannello
                const panelGeom = new THREE.BoxGeometry(
                    {lato_maggiore}, 
                    {lato_minore}, 
                    0.05
                );
                const panel = new THREE.Mesh(panelGeom, panelMaterial);
                panel.castShadow = true;
                panel.receiveShadow = true;
                panelGroup.add(panel);

                // Frame perimetrale
                const frameThickness = 0.08;
                const frameDepth = 0.06;
                
                // Frame superiore
                const frameTop = new THREE.Mesh(
                    new THREE.BoxGeometry({lato_maggiore}, frameThickness, frameDepth),
                    frameMaterial
                );
                frameTop.position.y = {lato_minore}/2;
                panelGroup.add(frameTop);
                
                // Frame inferiore
                const frameBottom = frameTop.clone();
                frameBottom.position.y = -{lato_minore}/2;
                panelGroup.add(frameBottom);
                
                // Frame sinistro
                const frameLeft = new THREE.Mesh(
                    new THREE.BoxGeometry(frameThickness, {lato_minore}, frameDepth),
                    frameMaterial
                );
                frameLeft.position.x = -{lato_maggiore}/2;
                panelGroup.add(frameLeft);
                
                // Frame destro
                const frameRight = frameLeft.clone();
                frameRight.position.x = {lato_maggiore}/2;
                panelGroup.add(frameRight);

                // Applicazione rotazioni
                panelGroup.rotation.x = -tiltRad;
                panelGroup.rotation.y = azimuthRad;

                // Posizionamento
                const heightOffset = {altezza_suolo} + ({lato_minore}/2) * Math.sin(tiltRad);
                panelGroup.position.set(x, heightOffset, z);

                return panelGroup;
            }}

            // Generazione array di pannelli
            const startX = -({campo_larghezza} / 2) + ({pitch_laterale} / 2);
            const startZ = -({campo_profondita} / 2) + (({lato_minore} + {carreggiata}) / 2);

            for (let row = 0; row < {num_rows}; row++) {{
                for (let col = 0; col < {num_panels_per_row}; col++) {{
                    const x = startX + col * {pitch_laterale};
                    const z = startZ + row * ({lato_minore} + {carreggiata});
                    const panel = createPanel(x, z);
                    scene.add(panel);
                }}
            }}

            // ========== CONTROLLI MOUSE ==========
            let isDragging = false;
            let isPanning = false;
            let previousMousePosition = {{ x: 0, y: 0 }};
            const rotationSpeed = 0.005;
            const panSpeed = 0.05;

            renderer.domElement.addEventListener('mousedown', (e) => {{
                if (e.button === 0) isDragging = true;
                if (e.button === 2) isPanning = true;
                previousMousePosition = {{ x: e.clientX, y: e.clientY }};
            }});

            renderer.domElement.addEventListener('mouseup', () => {{
                isDragging = false;
                isPanning = false;
            }});

            renderer.domElement.addEventListener('mousemove', (e) => {{
                if (isDragging) {{
                    const deltaX = e.clientX - previousMousePosition.x;
                    const deltaY = e.clientY - previousMousePosition.y;

                    const rotationQuaternion = new THREE.Quaternion()
                        .setFromEuler(new THREE.Euler(
                            deltaY * rotationSpeed,
                            deltaX * rotationSpeed,
                            0,
                            'XYZ'
                        ));

                    const currentPosition = camera.position.clone();
                    currentPosition.sub(scene.position);
                    currentPosition.applyQuaternion(rotationQuaternion);
                    currentPosition.add(scene.position);
                    camera.position.copy(currentPosition);
                    camera.lookAt(scene.position);
                }}

                if (isPanning) {{
                    const deltaX = (e.clientX - previousMousePosition.x) * panSpeed;
                    const deltaY = (e.clientY - previousMousePosition.y) * panSpeed;

                    const right = new THREE.Vector3();
                    camera.getWorldDirection(right);
                    right.cross(camera.up).normalize();

                    const up = new THREE.Vector3();
                    camera.getWorldDirection(up);
                    up.cross(right).normalize();

                    camera.position.addScaledVector(right, -deltaX);
                    camera.position.addScaledVector(up, deltaY);
                }}

                previousMousePosition = {{ x: e.clientX, y: e.clientY }};
            }});

            renderer.domElement.addEventListener('wheel', (e) => {{
                e.preventDefault();
                const zoomSpeed = 0.1;
                const direction = new THREE.Vector3();
                camera.getWorldDirection(direction);
                camera.position.addScaledVector(direction, -e.deltaY * zoomSpeed);
            }});

            renderer.domElement.addEventListener('contextmenu', (e) => e.preventDefault());

            // ========== ANIMAZIONE ==========
            function animate() {{
                requestAnimationFrame(animate);
                renderer.render(scene, camera);
            }}
            animate();

            // ========== RESPONSIVE ==========
            window.addEventListener('resize', () => {{
                camera.aspect = container.clientWidth / container.clientHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, container.clientHeight);
            }});
        </script>
    </body>
    </html>
    """
    
    return html_code


def display_3d_field(params: dict):
    """
    Visualizza il campo fotovoltaico in 3D nella pagina Streamlit
    
    Args:
        params: dizionario parametri impianto
    """
    st.markdown(
        '<p class="section-header" style="margin-top: 2rem;">Visualizzazione 3D Campo Fotovoltaico</p>',
        unsafe_allow_html=True
    )
    
    html_content = create_3d_field_visualization(params)
    components.html(html_content, height=620, scrolling=False)
    
    # Info aggiuntive sotto la visualizzazione
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"""
        **📐 Dimensioni Pannello**
        - {params.get('lato_maggiore', 0):.2f} × {params.get('lato_minore', 0):.2f} m
        - Area: {params.get('area_pannello', 0):.2f} m²
        """)
    
    with col2:
        st.info(f"""
        **📏 Spaziatura**
        - Pitch: {params.get('pitch_laterale', 0):.2f} m
        - Carreggiata: {params.get('carreggiata', 0):.2f} m
        """)
    
    with col3:
        st.info(f"""
        **🔧 Configurazione**
        - Altezza: {params.get('altezza_suolo', 0):.2f} m
        - Totale: {params.get('num_panels_total', 0)} pannelli
        """)
