# Rebuild the example pages and screenshots.
examples:
    cd examples/baby-names && python3 prepare.py && python3 build.py && ./screenshot.sh
