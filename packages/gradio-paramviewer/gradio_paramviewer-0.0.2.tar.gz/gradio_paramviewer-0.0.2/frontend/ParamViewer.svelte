<script lang="ts">
	export let docs;

	$: _docs = Object.entries(docs).map(([name, { type, description, default: _default }]) => {
    console.log({type, description, _default})
    return {
      name: name,
      type: type.dark,
      description: description,
      default: _default.dark,
    }
  })
	$: console.log(_docs)
	$: show_desc = _docs.map(x => false)

  const m = window.matchMedia('(prefers-color-scheme: dark)');
  m.matches ? handle_docs("dark") : handle_docs("light")

  m.addEventListener('change', e => {
    console.log(e)
    handle_docs(e.matches ? "dark" : "light")
  })

  function handle_docs(mode: "dark" | "light") {
    if (mode === "dark") {
      _docs = Object.entries(docs).map(([name, { type, description, default: _default }]) => {
        console.log({type, description, _default})
        return {
          name: name,
          type: type.dark,
          description: description,
          default: _default.dark,
        }
      })
    } else {
      _docs = Object.entries(docs).map(([name, { type, description, default: _default }]) => {
        console.log({type, description, _default})
        return {
          name: name,
          type: type.light,
          description: description,
          default: _default.light,
        }
      })
    }
  }
</script>

<div   class="wrap">
  {#if _docs}
    {#each _docs as { type, description, default: _default }, i}
      <div class="param" class:open={show_desc[i]}>
        <div class="type">{@html type} <span on:click={() => show_desc[i] = !show_desc[i]} class="arrow" class:hidden={!show_desc[i]}>▲</span></div>
        {#if show_desc[i]}

          <div class="default"><span>default</span> <code>=</code> {@html _default}</div>
          <div class="description"><p>{description}</p></div>
        {/if}
      </div>
    {/each}
  {/if}
</div>

<style>


	.default :global(pre), .default :global(.highlight) {
		display:inline-block;
		
	}

	.wrap :global(pre), .wrap :global(.highlight) {
		margin: 0;
		background: transparent !important;
		font-family: var(--font-mono);
		font-weight: 400;
		font-size: 0.9rem;
	}

	.default > span {
		text-transform: uppercase;
		font-size: 0.7rem;
		font-weight: 600;
	}
	code {
		background: none;
		font-family: var(--font-mono);
	}

	.wrap {
		/* background: #fff; */
		/* box-shadow: 0px 2px 8px #00000014; */
		padding: 0rem;
		border-radius: 5px;
		border: 1px solid #eee;
		overflow:hidden;
    position: relative;
		margin: 0;
		box-shadow: var(--block-shadow);
		border-width: var(--block-border-width);
		border-color: var(--block-border-color);
		border-radius: var(--block-radius);
		background: #fff;
		width: 100%;
		line-height: var(--line-sm);
    color: var(--body-text-color);
	}



	.type {
		/* background-color: hsl(206,64%,98%); */
		position: relative;
		/* border-bottom: 1px solid #eee; */
		padding: 1rem;
				/* background: rgb(255, 255, 224, 0.5); */
		/* background: darkorange; */
		/* color: white; */
    background: var(--neutral-900);
    background: var(--neutral-50);
    border-bottom: 1px solid var(--neutral-700);
    border-bottom: 0px solid var(--neutral-200);

	}

  

	.arrow {
		position: absolute;
		top: 0;
		bottom:0;
		right: 15px;
		transform: rotate(180deg);
		height: 100;
		display: flex;
		align-items: center;
		cursor: pointer;
	}

	.arrow.hidden {
		transform: rotate(270deg);
	}

	.default {
		padding: 0.2rem 1rem 0.3rem 1rem;
		border-bottom: 1px solid var(--neutral-700);
    border-bottom: 1px solid var(--neutral-200);

	
	}

	.description {
		padding: 1rem 1rem;
			

		font-family: var(--font-sans);
		font-weight: 500;
	}

  .param {
    border-bottom: 1px solid var(--neutral-200);
  }
 

  .param:last-child .description {
    border-bottom: none;
  }

  .open .type {
    border-bottom-width: 1px;
  }

  @media (prefers-color-scheme: dark) {
    .wrap {
      background: var(--neutral-800);
    }
    
    .default {
      border-bottom: 1px solid var(--neutral-700);
    }

    .type {
      background: var(--neutral-900);
      border-bottom: 0px solid var(--neutral-700);
    }

    
    .arrow {
      color: var(--neutral-200);
    }

    .param  {
      border-bottom: 1px solid var(--neutral-700);
    }

    .param:last-child  {
      border-bottom: none;
    }
  }

 
</style>