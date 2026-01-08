# COPR Makefile for building with rpmautospec support

srpm:
	dnf install -y rpmautospec-rpm-macros
	rpmautospec process-distgit
	rpmbuild -bs --define "_sourcedir $(PWD)" \
		--define "_specdir $(PWD)" \
		--define "_builddir $(PWD)" \
		--define "_srcrpmdir $(outdir)" \
		--define "_rpmdir $(outdir)" \
		$(spec)
